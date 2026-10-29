# R46bExecSelftestC2 — extended C2 selftest (mutant discrimination)

VERDICT: DRAFT-READY

Deliverable: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC2.draft/r46-counters-selftest-c2.py` — the COMPLETE extended selftest (sha256 `0457a1926d766d73297aa07b2997a4fd79037bed5201501e1310de3cd869c281`, 147 runtime cases = the committed 137 + 10 new). Draft only; nothing outside my draft dir and scratch was written. The committed `corpus/instruments/r46-counters-selftest-c2.py`, `r46-c2-gate.py`, `r46-mutbat.py` and the frozen claims were never edited.

## 1. What was built

The draft extends the committed selftest in exactly three regions (merge surface for the L1; no overlap with the sibling v1.3 draft's hunks):

1. A docstring paragraph after the `--do-nothing-control` paragraph (describes the ten `mut-g<N><x>-*` cases).
2. A module-level block inserted before `class Case:` — constants `MUT_XREF_FILE`, `MUT_LINK_FILE`, `MUT_PACK_A`, `MUT_PACK_B`, helper `_replace_first_line`, mutators `m_mut_f28_sources_cell`, `m_mut_verified_at_prefix`, `m_mut_limits_word_floor`, `m_mut_overlap_xref_swapped`, `m_mut_registry_row_cells`, `m_mut_manifest_quote_count`, `m_mut_knowledge_symlink`, `m_mut_sources_symlink`, `m_mut_entry_byte_floor`, `m_mut_five_cores_two_spans`, `g5c_entry_text`.
3. Ten `add(Case("mut-g…", "mutant", …))` registrations immediately after the `ctl-committed-tip-direct` control.

Each new case is a tree the FROZEN counter rejects on its targeted gate and on no other gate (except `allow=`), and on which the matching `r46-mutbat.py` C2 mutant turns that gate green — so the selftest fails under that mutant and the battery records it caught. Mutants still uncaught at freeze: 13 (frozen before-value receipt `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`). Ten are now discriminated: G1c, G2a, G2b, G2c, G3a, G4b, G5c, G6a, G6c, G7b. Three are argued equivalent: G6b, G7a, G7c (§3).

## 2. Per-mutant verification (performed)

Command (all ten cases, frozen counter = lane tip `r46-c2-gate.py` v1.2 vs the mutbat's own mutant line, same tree):

```
SCRATCH=/fast/scratch/hyaku/kasegi-r46/R46bExecSelftestC2 python3 /fast/scratch/hyaku/kasegi-r46/R46bExecSelftestC2/verify_cases.py
```

Harness (kept in my scratch, quoted in full in the hand-off): builds the synthetic tree via the selftest's own `build()` from `--pure`-equivalent `/fast/scratch/hyaku/kasegi-r46/L1/pure2`, applies the case mutator, runs the frozen counter and the mutant counter (the mutbat's exact `old→new` line, placed at `<tmp>/corpus/instruments/gate-<id>.py` so `TOOL_ROOT` resolves as the battery does it), and for the repin case sets `R46_PINS_OVERRIDE` exactly as `run_case` does. Printed output (verbatim):

```
mut-g1c-f28-sources-cell-prefix    G1c-src-boundary       frozen failing=['G1']         fixed=6/7 | mutant failing=[]             fixed=7/7 | OK
mut-g2a-verified-at-prefix         G2a-verified-prefix    frozen failing=['G2']         fixed=6/7 | mutant failing=[]             fixed=7/7 | OK
mut-g2b-limits-word-floor          G2b-wordfloor-low      frozen failing=['G2']         fixed=6/7 | mutant failing=[]             fixed=7/7 | OK
mut-g2c-overlap-xref-swapped       G2c-need-empty         frozen failing=['G2']         fixed=6/7 | mutant failing=[]             fixed=7/7 | OK
mut-g3a-registry-row-cells         G3a-cells-loose        frozen failing=['G3', 'G7']   fixed=5/7 | mutant failing=['G7']         fixed=6/7 | OK
mut-g4b-manifest-quote-count       G4b-quotes-low         frozen failing=['G4']         fixed=6/7 | mutant failing=[]             fixed=7/7 | OK
mut-g5c-five-cores-two-spans       G5c-pass-low           frozen failing=['G3', 'G4', 'G5'] fixed=4/7 | mutant failing=['G3', 'G4']   fixed=5/7 | OK
mut-g6a-knowledge-file-symlink     G6a-guards-dead        frozen failing=['G6']         fixed=6/7 | mutant failing=[]             fixed=7/7 | OK
mut-g6c-entry-byte-floor           G6c-size-low           frozen failing=['G6']         fixed=6/7 | mutant failing=[]             fixed=7/7 | OK
mut-g7b-sources-md-symlink         G7b-symlink-dead       frozen failing=['G7']         fixed=6/7 | mutant failing=[]             fixed=7/7 | OK
discriminating cases: 10/10
```

In every row the frozen counter's failing set is exactly targets ∪ allow (so the case passes at baseline: `miss=∅`, `extra=∅`, `fixed≠7`) and the mutant flips exactly the targeted gate. Notes per case:

- **G1c** — F28 row sources cell `S0730`: the frozen `\bS073\b` rejects, the mutant's plain substring accepts.
- **G2a** — `verified-at: 2026-10-28T00:00:00Z`: the frozen whole-line compare rejects, the mutant's `startswith` accepts.
- **G2b** — Limits section rewritten to 13 words: below the frozen 25-word floor, above the mutant's 5-word floor; anchored/floors otherwise intact.
- **G2c** — the entry's second xref repointed at `corpus/knowledge/claim-anatomy-sample.md:1` (existing, non-exempt, non-entry): `need ⊄ have` under the frozen need-set; the mutant's `need = set()` only checks `refok == len(refs)`, which still holds.
- **G3a** — a twelfth cell appended to the S073 row (allow={G7}: the census reads the same 12-cell row, so G7 trips under both counters; the census is the only extra failure).
- **G4b** — manifest with Q2 removed → 7 verified quotes; `repin=True` (the harness's own grader-side override) pins the edited manifest so only the `oks >= 8 → >= 1` limb can fire. Frozen: `quotes-ok=7` red; mutant: green.
- **G5c** — two located spans carry all five frozen cores (`MUT_PACK_A` covers cores 1–3 at line 560, `MUT_PACK_B` covers cores 4–5 at line 561, 25 and 23 words). The pinned capture keeps the closest core pair 30 words apart (>25, so no span can carry two cores), which is why this case doctors the capture and trips the capture's own pins G3/G4 as allowed collateral; frozen G5 red `located=2`, mutant green.
- **G6a** — `corpus/knowledge/citation-bases.md` replaced by a symlink to a byte-identical copy in `corpus/knowledge-linktarget/`: `base_ok` and the name/content pins hold, the frozen `links` guard rejects, the mutant's dead guard accepts.
- **G6c** — entry trimmed under the 3000-byte floor (pad line removed, Scope and Overlap prose shortened; every other limb stays green, verified: the only frozen failure is G6).
- **G7b** — `corpus/SOURCES.md` symlinked to `SOURCES-copy.md` in the same directory: the census validates the copy (`census-rc=0 ok-line=1`), the frozen `census-input-is-a-symlink` guard rejects, the mutant accepts.

## 3. The three remaining mutants — equivalent-on-battery, with the argument

- **G6b-integrity-loose** (drops `len(everything)==65 and nested==65`): `base_ok` pins `base_like`'s names to the round-45 tip's 64 names, so with the entry file present (forced by `sized`) `everything` is exactly those 64 + the entry name = 65; a subdirectory would have to be a 66th name or would displace a file (then `names ≤ 64`), so `nested == 65` whenever `base_ok ∧ names==65`. Empirical check — command `SCRATCH=… python3 probe_equivalence.py`, battery of 13 knowledge-directory mutations (extra .md, stray .txt, nested .md, delete, rename, byte change, entry deleted/symlinked/truncated, base file symlinked / replaced by a directory, knowledge dir symlinked): printed `G6 readings differing between frozen and mutant: 0`.
- **G7a-verdict-or** (`rc == 0 and ok_line → or`) and **G7c-okline-loose** (`^\S+\tok\t → ^\S+\tok`): under the census script (sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`) in validate mode with a single `--file` lane, the ok line is emitted iff the lane has no E-codes, and rc==1 iff findings (E-codes), so `rc==0 ⇔ ok_line`; and the only line the census emits containing a tab-"ok" is the ok line `"$lane\tok\t$f"`, which ends in a tab, so the strict and loose regexes match exactly the same lines. Empirical check (same command): battery of 14 registry mutations, printed `census-rc`, `ok-strict`, `ok-loose` and `rc==0 <=> ok-line: yes` on every row, plus `G7 readings differing between frozen and the two mutants: 0`.

These two arguments are scoped to the census bytes above; if the fleet-root census changes, G7a/G7c must be re-examined. I did NOT commit equivalence proof files — the L1 owns the `--equivalent` map and the committed proofs at integration; the probe script and its full output are preserved in my scratch (copied into the draft dir, §5).

## 4. Baseline

- Extended draft, full run (performed): `HYAKU_SCRATCH=/fast/scratch/hyaku/kasegi-r46/R46bExecSelftestC2 python3 <draft> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --keep` — exit 0, wall 271 s, final lines (verbatim, full log in the draft dir as `selftest-baseline-147.txt`):
  ```
  selftest cases=147 failures=0
  ```
  So all 137 committed cases and the 10 new cases pass at baseline against the frozen v1.2 counter. (The committed 137-case file's own `failures=0` at the frozen base is additionally the frozen before-value in `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`; not re-run separately.)
- Full `r46-mutbat.py --counter both` battery pass: NOT started (L1 instruction not to start new full battery passes).

## 5. Scratch and hand-off

Receipts copied into my draft dir: `selftest-baseline-147.txt` (full 147-case run log), `per-mutant-verification.txt` (frozen-vs-mutant table of §2), `equivalence-probe.txt` (G6b/G7a/G7c batteries of §3). The generator and harness scripts stay only in my scratch and are removed at yield; the draft file is self-contained. No tool installs were made (none needed).

Merge note for the L1: this draft is based on the committed v1.2-gate selftest and passes under both the v1.2 and the v1.3 semantics (the sibling's five edits touch disjoint regions; none of my cases depends on the C1 ledger exemption: `claim-anatomy-sample.md` and `citation-bases.md` are non-exempt, and all byte pins hold in both variants).

## Limitations

- The full battery pass was not run within the wave window (see §4); the L1 should run `r46-mutbat.py --counter c2` at integration and expect the ten mutants of §2 caught and G6b/G7a/G7c needing the `--equivalent` map with committed proofs.
- The G7a/G7c equivalence is conditioned on the census script sha256 above; the G5c and G3a cases carry allowed collateral (G3+G4 and G7 respectively) because the discriminating tree necessarily trips those pins.
