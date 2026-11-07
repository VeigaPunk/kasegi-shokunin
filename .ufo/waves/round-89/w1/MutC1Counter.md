# MutC1Counter — mutation test of the round-89 C1 counter

| field | value |
|---|---|
| seat | MutC1Counter (leaf, w1, round 89 attempt 1) |
| instrument | `.ufo/waves/round-89/c1/knowledge-meter.py` sha256 `6e8a6b7661f4b7c82b46e8b82f769c38d5a88b1021baaa3a60c2440773092bc7` (unchanged before and after this probe) |
| base / freeze | `090a46f89932324787e00ca20b1007f893934c9a` / `94573d2573dc6cca83454cc65b787d37d96988f5` |
| detector | the frozen pre-freeze control set, `.ufo/waves/round-89/controls/c1-controls-r89.sh` (9 meter invocations), re-created tree by tree in scratch |
| mutants | 37 (M9 14, M4 6, M5 4, M1 2, M2 2, M3 5, M7 2, commit-bound read 2) |
| killed by the frozen control set alone | **11/37 = 29.7%** (8 detection kills, 3 killed because the positive control stops passing) |
| additional executed plants | 14 plants; 13 of the 26 survivors die on one |
| survive both | 13 (structural / redundant guards, §6) |

## 1. Method

Pristine counter copied to scratch as `c0.py` (sha256 `6e8a6b7661f4b7c82b46e8b82f769c38d5a88b1021baaa3a60c2440773092bc7`). Every mutant is an exact
single-point replacement of that text (no re-implementation); each replacement string was asserted
to occur exactly once. The detector is the frozen control repertoire with the same command lines as
`c1-controls-r89.sh`, with one fixture tree per control built exactly as that script builds it:
`git clone -q --shared <lane> $S/<tree>` + `git -C <tree> checkout -q 090a46f89932324787e00ca20b1007f893934c9a` (toplevel asserted to be the
clone), the frozen `apply-map.py`, and one fixture commit (`fixture <fixture@invalid>`), plus the
forged / shifted-label / out-of-range map+labels files the script derives.

Judging rule: a mutant is **killed by the frozen set** when any of the nine invocations changes a limb
verdict or the verdict line relative to the pristine image — either a limb that must FAIL starts
passing (detection lost) or the positive control's limbs stop passing (mutant over-strict; not a
detection win, flagged as such). A mutant with no delta on all nine is **SURVIVED**, and I then ran a
planted case that the frozen set lacks. Rate = the frozen `785/1797` for every pristine image.

Qualifier baked into the plants: each plant's `--target` is the after rate *measured on that tree*
with the pristine counter, so M1 is never the discriminator in a plant run.

## 2. Fidelity of the re-created control trees

All nine pristine images (LIMB + KNOWLEDGE-METER lines) are byte-identical substrings of
`.ufo/waves/round-89/controls/c1-controls-r89.txt`, asserted programmatically
(receipt `MutC1Counter-receipts/baseline-controls.txt`). Expected limb images reproduced:
do-nothing and working-tree-only fail M1/M2/M3; prefix forgery fails M9 (5 keys) and, pinned, M6/M7;
shifted label line fails M9 on one key; extra repoint fails M1/M2/M3; cited-entry shift fails M3;
out-of-range fails M5 and M9.

## 3. Results — 37 mutants

| # | mutant | area | frozen control set | planted case (executed) |
|---|---|---|---|---|
| 1 | `M1-01-num-only` | M1 target equality | SURVIVED | none constructible — see §6 |
| 2 | `M1-02-ge` | M1 target equality | C7-extra-repoint M1 FAIL->pass | — |
| 3 | `M2-01-added-drop` | M2 stray-added check | SURVIVED | P10 kills it (a fresh GONE citation at after-rev with no map entry) |
| 4 | `M2-02-removed-superset` | M2 stray-removed check | SURVIVED | P11 kills it (an unlabelled repoint whose value is already a map value) |
| 5 | `M3-01-lenient-len` | M3 line-count equality | C8-cited-shift M3 FAIL->pass (verdict flips) | — |
| 6 | `M3-02-mismatch-ignored` | M3 line equality | C1-do-nothing M3 FAIL->pass; C3-worktree-only M3 FAIL->pass; C7-extra-repoint M3 FAIL->pass | — |
| 7 | `M3-03-samefiles-true` | M3 file-set equality | SURVIVED | P9 kills it (a new corpus/knowledge/extra-entry.md at after-rev) |
| 8 | `M3-04-hit-drop` | M3 key-coverage | SURVIVED | none constructible — see §6 |
| 9 | `M3-05-replace-bare` | M3 replacement form | SURVIVED | none constructible — see §6 |
| 10 | `M4-01-nameeq-drop` | M4 basename equality | SURVIVED | P5 kills it (value corpus/knowledge/ops-invariants.md:35 for key claim-gates.md:34) |
| 11 | `M4-02-gone-drop` | M4 key-GONE-in-base | SURVIVED | none constructible — see §6 |
| 12 | `M4-03-unique-drop` | M4 basename uniqueness | SURVIVED | P7 kills it (docs/claim-gates.md tracked beside corpus/knowledge/claim-gates.md) |
| 13 | `M4-04-internal-drop` | M4 INTERNAL classification | SURVIVED | none constructible — see §6 |
| 14 | `M4-05-val-prefix-optional` | M4 VAL prefix | SURVIVED | none constructible — see §6 |
| 15 | `M4-06-key-leading-dot` | M4 KEY regex | SURVIVED | none constructible — see §6 |
| 16 | `M5-01-hi-drop` | M5 upper bound | C9-oor M5 FAIL->pass | — |
| 17 | `M5-02-order-drop` | M5 range order | SURVIVED | P12 kills it (reversed range :85-81 inside the entry) |
| 18 | `M5-03-slack` | M5 EOF slack | SURVIVED | P13 kills it (range :160-161 one line past EOF) |
| 19 | `M5-04-lo-zero` | M5 lower bound | SURVIVED | P14 kills it (range :0-3) |
| 20 | `M7-01-hash-uses-map` | M7 labels digest | C1-do-nothing M7 pass->FAIL; C2-positive M7 pass->FAIL; C3-worktree-only M7 pass->FAIL; C7-extra-repoint M7 pass->FAIL; C8-cited-shift M7 pass->FAIL (verdict flips) | — |
| 21 | `M7-02-always-true` | M7 pin comparison | C5-prefix-pinned M7 FAIL->pass | — |
| 22 | `M9-01-classmark-lax` | M9 class marks | SURVIVED | none constructible — see §6 |
| 23 | `M9-02-wrongsame-drop` | M9 WRONG-different rule | SURVIVED | P1 kills it (two WRONG rows left at their own anchor (their review lines carry that anchor token)) |
| 24 | `M9-03-fnsame-drop` | M9 FN-same rule | SURVIVED | none constructible — see §6 |
| 25 | `M9-04-mapeq-drop` | M9 map==labels equality | SURVIVED | P2 kills it (labels row deleted: a map pair no non-author named) |
| 26 | `M9-05-anchor-unbound` | M9 L-token limb | C9-oor M9 FAIL->pass | — |
| 27 | `M9-06-token-right-noboundary` | M9 L-token right boundary | SURVIVED | none constructible — see §6 |
| 28 | `M9-07-token-left-noboundary` | M9 L-token left boundary | SURVIVED | none constructible — see §6 |
| 29 | `M9-08-cell-loose` | M9 table-cell binding | SURVIVED | none constructible — see §6 |
| 30 | `M9-09-wholefile-line` | M9 named-line binding | C6-shifted-label M9 FAIL->pass (verdict flips) | — |
| 31 | `M9-10-class-drop` | M9 class validation | SURVIVED | P4 kills it (labels row with class MAYBE) |
| 32 | `M9-11-anchor-range-collapse` | M9 anchor range form | C1-do-nothing M9 pass->FAIL; C2-positive M9 pass->FAIL; C3-worktree-only M9 pass->FAIL; C7-extra-repoint M9 pass->FAIL; C8-cited-shift M9 pass->FAIL (verdict flips) | — |
| 33 | `M9-12-dupe-len-drop` | M9 duplicate-row guard | SURVIVED | P3 kills it (the same pair listed on two labels rows) |
| 34 | `M9-13-class-lookup-drop` | M9 class marks (redundant guard) | SURVIVED | none constructible — see §6 |
| 35 | `M9-14-class-validation-drop` | M9 class marks | SURVIVED | P4 kills it (labels row with class MAYBE) |
| 36 | `P-01-afterrev-worktree` | commit-bound after-rev read | C3-worktree-only M1 FAIL->pass; C3-worktree-only M2 FAIL->pass; C3-worktree-only M3 FAIL->pass (verdict flips) | — |
| 37 | `P-02-baserev-worktree` | commit-bound base-rev read | C2-positive M2 pass->FAIL; C2-positive M3 pass->FAIL; C2-positive M4 pass->FAIL; C2-positive M5 pass->FAIL; C3-worktree-only M4 pass->FAIL; C3-worktree-only M5 pass->FAIL; C4-prefix-unpinned M2 pass->FAIL; C4-prefix-unpinned M3 pass->FAIL; C4-prefix-unpinned M4 pass->FAIL; C4-prefix-unpinned M5 pass->FAIL; C5-prefix-pinned M2 pass->FAIL; C5-prefix-pinned M3 pass->FAIL; C5-prefix-pinned M4 pass->FAIL; C5-prefix-pinned M5 pass->FAIL; C6-shifted-label M2 pass->FAIL; C6-shifted-label M3 pass->FAIL; C6-shifted-label M4 pass->FAIL; C6-shifted-label M5 pass->FAIL; C7-extra-repoint M4 pass->FAIL; C7-extra-repoint M5 pass->FAIL; C8-cited-shift M2 pass->FAIL; C8-cited-shift M4 pass->FAIL; C8-cited-shift M5 pass->FAIL; C9-oor M2 pass->FAIL; C9-oor M3 pass->FAIL; C9-oor M4 pass->FAIL (verdict flips) | — |

## 4. Kill ratio, frozen control set alone

| area | mutants | killed | note |
|---|---|---|---|
| M9 label binding | 14 | 3 (M9-05, M9-09, M9-11) | only the `oor` control (anchor token) and the `shifted-label` control (named line) reach M9; M9-11 is an over-strict kill |
| M4 binding | 6 | **0** | no control ever puts a bad value, a non-GONE key, a second basename or a non-INTERNAL target in front of M4 |
| M5 range | 4 | 1 (M5-01, by `oor`) | the three range-shape weakenings (order, EOF slack, line 0) are untouched |
| M1 target | 2 | 1 (M1-02, by `extra-repoint`) | numerator-only comparison is untouched |
| M2 token sets | 2 | **0** | `extra-repoint` trips both conjuncts at once, so neither is isolated |
| M3 line diff | 5 | 2 (M3-01, M3-02) | file-set and key-coverage weakenings untouched |
| M7 labels pin | 2 | 2 | — |
| commit-bound read | 2 | 2 | `after-rev` read replaced by the working tree dies on `working-tree-only`; `base-rev` replaced dies on the positive control |

8/37 (21.6%) are detection kills; 3/37 die only because the positive control stops passing
(`M7-01-hash-uses-map`, `M9-11-anchor-range-collapse`, `P-02-baserev-worktree`) — those are dead
mutants, not evidence of detection.

## 5. Survivors the frozen set misses but a plant kills (13)

Evidence: `MutC1Counter-receipts/plants.txt` (pristine vs mutant limb images per plant).
P8 also reproduces `M3-01-lenient-len`'s frozen kill (cross-check only; that mutant is counted in §4,
not here), and P6 kills nothing by design (§6).

| plant | defect the frozen set never shows the counter | mutants it kills | baseline | under mutant |
|---|---|---|---|---|
| P1 | two WRONG pairs left at their own anchor whose review lines happen to carry that anchor (`claim-gates.md:34`, `:63-66`) | `M9-02-wrongsame-drop` | M9 FAIL | whole run pass |
| P2 | a labels file missing one row (map pair no non-author named) | `M9-04-mapeq-drop` | M9 FAIL | whole run pass |
| P3 | the same pair on two labels rows | `M9-12-dupe-len-drop` | M9 FAIL | whole run pass |
| P4 | a labels row with class `MAYBE` | `M9-14-class-validation-drop`, `M9-10-class-drop` | M9 FAIL | M9-14 whole run pass; M9-10 aborts `KeyError: 'MAYBE'` rc=1 (fail-closed, no verdict line) |
| P5 | value `corpus/knowledge/ops-invariants.md:35` for key `claim-gates.md:34` | `M4-01-nameeq-drop` | M4+M5 FAIL | whole run pass |
| P6 (control, kills nothing) | value `corpus/claim-gates.md:35` (no `knowledge/` segment) | `M4-05-val-prefix-optional` | M4+M5+M9 FAIL | M4 still FAIL — the lax prefix is closed by the INTERNAL conjunct; this is the evidence in §6 |
| P7 | `docs/claim-gates.md` tracked beside the knowledge entry | `M4-03-unique-drop` | M4+M5 FAIL | whole run pass |
| P8 | a line appended at the end of `claim-gates.md` | `M3-01-lenient-len` | M3 FAIL | whole run pass |
| P9 | a new `corpus/knowledge/extra-entry.md` at after-rev | `M3-03-samefiles-true` | M3 FAIL | whole run pass |
| P10 | a fresh GONE citation at after-rev with no map entry | `M2-01-added-drop` | M2+M3 FAIL | M2 passes, M3 still FAIL |
| P11 | an unlabelled repoint whose value is already a map value | `M2-02-removed-superset` | M2+M3 FAIL | M2 passes, M3 still FAIL |
| P12 | reversed range `:85-81` inside the entry | `M5-02-order-drop` | M5+M9 FAIL | M5 passes, M9 still FAIL |
| P13 | range `:160-161`, one line past the 160-line EOF | `M5-03-slack` | M5+M9 FAIL | M5 passes, M9 still FAIL |
| P14 | range `:0-3` | `M5-04-lo-zero` | M5+M9 FAIL | M5 passes, M9 still FAIL |

P2/P3/P4 matter most: they are exactly the failure modes M9 was introduced to catch (a pair no
non-author named; a transcription duplicate; a wrong class), and the frozen control set cannot
distinguish a counter that has stopped enforcing them.

## 6. Survivors no plant can reach (13)

| mutant | why the limb is unreachable for this claim |
|---|---|
| `M1-01-num-only` | no control lands on numerator 785 with a denominator other than 1797 (measured images: 777/1798, 785/1797, 784/1796, 786/1797). The denominator is fixed by M2+M4 once `removed == keys` and every value is INTERNAL, so the r88 rate-gaming shape 785/1798 is caught by M2 (stray_added) or M3. [INFERENCE from the limb definitions plus the measured images] |
| `M3-04-hit-drop` | `hit == keys` is implied by M4: resolve.collect only yields tokens inside backticks (TOKEN = `` `([^`\n]+)` ``), so a key that classifies GONE necessarily occurs backticked in the base scope, which is exactly what `hit` records. |
| `M3-05-replace-bare` | the guard that requires the backticked form to be present on the line is untouched, so the lax replacement only differs on a base line that holds a backticked map key *and* a bare/qualified twin of a key. Measured: 0 such lines in corpus/knowledge/*.md at base. |
| `M4-02-gone-drop` | all nine label rows bind keys that are GONE at base (baseline M4 pass), and M9 admits only rows whose review line carries **WRONG or `proxy false negative`; the frozen review has no such row for an INTERNAL key. A map entry keyed on an already-correct citation is unobservable to the frozen set (P2-style plants do not cover it). |
| `M4-04-internal-drop` | with mirror_absent=True, resolve.classify over VAL-legal relative paths returns only INTERNAL or GONE (MIRROR-EQUIVALENT needs the mirror root; RESOLVES needs `~` or `/`), so `!= "GONE"` is equivalent to `== "INTERNAL"` today. Equivalence, not a detection gap. |
| `M4-05-val-prefix-optional` | the lax prefix still needs classify(v) == INTERNAL, i.e. a bare `corpus/<name>.md` must exist, and `bybase[name] == [corpus/knowledge/<name>]`; if the bare twin exists, uniqueness fails. Measured on P6: the mutant still fails M4 because corpus/claim-gates.md does not exist (GONE). |
| `M4-06-key-leading-dot` | no dot-prefixed backticked citation exists in corpus/knowledge/*.md at base (grep, 0 hits), so a key such as `.claim-gates.md:34` has no GONE base token to bind; KEYS with a leading dot are unreachable from this corpus. |
| `M9-01-classmark-lax` | every WRONG row's review line carries `**WRONG`; relaxing the marker to `WRONG` changes no row. A plant needs a WRONG row marked with a weaker string (e.g. plain `WRONG`) — the frozen review at d0d9f49 has none. |
| `M9-03-fnsame-drop` | FN rows in labels.tsv are prefix repoints, and each FN review line's only L-token equals that anchor (inventory: :103 -> L10-11, :106 -> L15, :107 -> L9-16, :116 -> L17-25). `FN and not same` can only become true with a review line carrying a *different* anchor; none exists. |
| `M9-06-token-right-noboundary` | no labelled line's anchor is a proper prefix of another L-token on that line (inventory: :45 L34,L35 / :46 L36-37,L37 / :48 L63-66,L78-80 / :49 L66,L67,L81-85 / :54 L28,L29,L52-53 / :103,:106,:107,:116 single-token). Dropping `(?![\w-])` is inert for this label set; zero delta on all nine controls. |
| `M9-07-token-left-noboundary` | same inventory: no anchor occurs as a proper suffix of another L-token on its line, so dropping `(?<![\w-])` is inert. |
| `M9-08-cell-loose` | 0 review lines name a labelled key outside a `| key |` cell while also carrying the class marker and the anchor (measured over the whole review), so the cell check cannot be relaxed observably. |
| `M9-13-class-lookup-drop` | the early `c not in CLASS_MARK` guard is redundant with the later marker lookup; dropping only the marker lookup leaves class validation in place (P4 still FAILs M9). Dropping both is M9-14, which P4 kills. |

These are redundant-guard or dead-code findings, not permission to change the contract: the limbs
still hold for the frozen inputs.

## 7. Qualifiers routed (not re-scoring; the frozen predicates decide the claim)

1. **M9 binds the value's anchor, not the value's file.** In P5 the labels row
   (`claim-gates.md:34` -> `corpus/knowledge/ops-invariants.md:35`, review line 45, which does carry
   `L35`) passes M9 in *every* run including pristine; only M4's basename equality rejects the pair.
   So "labelled by a non-author" means the anchor matched the review, not that the reviewer endorsed
   that file. For the frozen map both happen to agree (all nine values keep their key's basename), so
   nothing about C1 changes; a future tranche should check the filename in M9 as well.
2. **`classify()` resolves against the lane checkout, not the rev.** Adding `docs/claim-gates.md` to a
   fixture flipped three already-cited tokens (`docs/`, `docs/*`, `docs/*.md`) GONE->INTERNAL and moved
   the measured base rate 777/1798 -> 780/1798 for the same rev (receipt
   `MutC1Counter-receipts/classify-lane-tree.txt`). The commit-bound property covers the scope *bytes*
   only. Harmless for C1 (the landing touches one knowledge file), but M1's number is not a pure
   function of the two revs.
3. **The counter is silent on M4 by construction of the controls**: 0/6 M4 mutants killed, and the
   round-89 novelty lives in M4 (re-anchor, uniqueness, INTERNAL). P5/P7 show the limb does work; the
   frozen set simply never exercises it.
4. `M9-02`'s WRONG-different conjunct is only partly decisive: in the frozen prefix forgery three of
   the five WRONG rows are caught by the anchor token instead (their forged anchors are ranges the
   review line never writes), which is why dropping the conjunct changes no limb verdict — the
   `unbound=` list merely shrinks from 5 keys to 3.

## 8. Restoration and hygiene

- The lane tree was read-only for this seat: no file under
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin` was written except this report and its receipts; the
  counter's bytes were re-hashed after the probe and are still `6e8a6b7661f4b7c82b46e8b82f769c38d5a88b1021baaa3a60c2440773092bc7`.
- All fixtures, clones, mutants and plant trees lived under `/fast/scratch/hyaku/kasegi-r89/MutC1Counter`
  and that directory was deleted before yield. `TMPDIR` was passed explicitly for every run; nothing was
  written to `/tmp`, `~/.local/bin`, the fleet repo or any sibling lane.
- No git/jj mutation touched the lane: clones were made *from* it, and the only commits are inside
  scratch clones with `git -C <clone>` after asserting `rev-parse --show-toplevel` equals the clone.
- No credential-shaped strings exist in this probe (no tokens, keys or signatures were created or
  copied); the receipts carry limb images and sha256 digests only.
- No tool was installed or upgraded.

Re-run: `bash .ufo/waves/round-89/controls/c1-controls-r89.sh <scratch>` reproduces §2 (the frozen
detector). Each mutant is one `old ==> new` replacement from the table in
`MutC1Counter-receipts/mutants.tsv`; run it as
`python3 -B <mutant>.py --lane <clone> --base-rev 090a46f89932324787e00ca20b1007f893934c9a --after-rev HEAD --map <map> --labels <labels> --target 785/1797 [--map-sha256 ..] [--labels-sha256 ..] --work <scratch>/w`.
