# Causal — C1/C2 independent-verifiability audit (round 23)

Seat: `KasegiR23.Causal-5`, read-only. Target: prove/falsify that C1 and C2 are
independently verifiable with no source-restoration dependency (C1) and no
unverifiable recheck dependency (C2), and that they are separable from each
other. Base `922a4dde90b60b465e2b8b241d1fe363f1f27e98`. No edits, no checks run.
All line numbers are working-tree bytes at read time (resolve.py is unmodified:
`git status` shows only SCORECARD/QUALITY modified + untracked wave outputs).

## Verdict up front

Both claims are *structurally* independent and *locally* verifiable in
principle. Neither is verifiable as written:

- C1's `after` contract ("all declared mirror-escape and prefix-confusion
  fixtures classify GONE") contradicts the suite's own expected classes and
  misses the literal-hit sub-case, and its guard conflates C2's corpus growth
  with C1's verdict flips.
- C2's executable rechecks currently fail closed at exit 2 because
  `corpus/source-snapshots/round-23/manifest.json` does not exist; the
  manifest↔entry quote binding and the manifest↔snapshot digest binding are
  nowhere asserted.

## C1 — evidence and counterexamples

`resolve.py` at base (unmodified; lines cited to current tree):

1. **Before-state is fixture-only, never host-reproducible.**
   `classify` reads the live FS via `exists_any` (resolve.py:204-213, 227-233)
   and `MIRROR_ROOT` is derived at import from `$KASEGI_MIRROR`/existing
   candidates (resolve.py:99-110). On the live host the mirror is absent
   (`before-instruments.json` reports `mirror=0` over 1589 distinct cites), so
   `~/Projects/bounties/../outside.md` → `GONE`, not the claimed
   `MIRROR-EQUIVALENT`. The `before_observed` is true only inside a fixture env
   (isolated `HOME` + `KASEGI_MIRROR`, as `test_resolve.py:106-135` builds).
   Claims.json does not freeze that environment or the fixture matrix.
   **Smallest correction:** the committed JSON fixture matrix (already in the
   CountMirror brief) must be named in the claim's evidence and must pin
   `HOME`, `KASEGI_MIRROR`, and the file layout; without it "identical fixture
   inputs" is an assertion, not a check.

2. **Strongest counterexample — literal-hit escape survives the planned
   confinement.** In the bounty branch, `exists_any(base)` runs *before* the
   mirror fallback (resolve.py:207-209). `expanduser` collapses `..`, so if
   `~/Projects/outside.md` exists, `~/Projects/bounties/../outside.md` returns
   `RESOLVES` and the confined fallback is never reached. The FixMirror brief
   confines the *fallback* joins; the literal first-hit still credits a file
   outside both the bounty root and the mirror — the very token in
   `before_observed` keeps a credit class (renamed RESOLVES).
   **Falsifier:** fixture with `~/Projects/outside.md` present; post-fix it is
   RESOLVES, not GONE.
   **Smallest correction:** either (a) normalize/contain the bounty-prefixed
   `base` itself (`realpath` must stay under the bounty root before the literal
   exists test), or (b) narrow the claim to "mirror fallback cannot credit
   escapes" and explicitly record the literal-hit carve-out like the
   lane-relative `INTERNAL` one already disclosed.

3. **`after` wording is wrong for prefix-confusion fixtures.** The suite's own
   expected class for an existing prefix sibling is `RESOLVES` as an ordinary
   other-root
   (`test_prefix_sibling_roots_keep_other_root_behavior`,
   test_resolve.py:210-218 — `the-bounty-hunter-legacy/README.md` → RESOLVES).
   "All declared mirror-escape and prefix-confusion fixtures classify GONE" is
   false for that control; if the matrix only includes absent siblings it is
   vacuous.
   **Smallest correction:** "escape fixtures classify GONE; existing
   sibling-root controls keep ordinary-root classes and never a mirror class."

4. **Bounty prefix has no boundary check — the live sibling-confusion
   `under_mirror` cannot fix.** `base.startswith(BOUNTY_PREFIXES)`
   (resolve.py:204) matches `~/Projects/bounties-legacy/x.md`;
   `split("/Projects/bounties",1)[1]` gives `-legacy/x.md` (`lstrip("/")` does
   not remove `-`), so `mirror_root/-legacy/x.md` → `MIRROR-EQUIVALENT` for a
   file whose mirror path does not correspond to the cited bounty path. The
   confinement target sits *inside* the mirror, so realpath containment passes.
   `mirror_suffix` does enforce `root + "/"` (resolve.py:185-190); the bounty
   branch needs the same. (FixMirror's brief does assign this boundary —
   recorded here because claims.json's "sibling-root prefix confusion" does not
   name the bounty side explicitly; verifier should require a
   `bounties-*` fixture row.)

5. **First-hit-vs-confinement semantics change.** `exists_any` returns the
   first match (literal → brace → glob, resolve.py:163-177). After confinement,
   a *first* match outside the mirror yields GONE even when a later confined
   match exists — conservative, fail-closed, acceptable — but it silently
   changes r15's "any match counts" behavior. The missing-file controls
   (relative precedence, test_resolve.py:221-235) pin which semantics survive;
   the claim should say which the matrix pins.

6. **C1↔C2 guard conflation (the independence defect).** C1's guard diffs
   "frozen pre-round SKILL and corpus against each detector." C2 lands three
   new `corpus/knowledge/*.md` + SOURCES/README rows — all inside the corpus
   `collect()` walks (resolve.py:250-276). A pre-corpus × post-detector-vs-
   post-corpus run mixes C2-added tokens (new INTERNAL/GONE rows) with C1
   verdict flips. `before-instruments.json` already uses
   `git archive 922a4dde` for "before"; the "after" resolver must also run
   against that same exported corpus for attribution, with corpus-growth deltas
   reported separately.
   **Smallest correction:** declare the no-harm corpus frozen at the base
   export; attribute verdict changes only over identical citation sets.

## C2 — evidence and counterexamples

7. **Recheck target file does not exist → every recheck exits 2 today.**
   All three new entries declare
   `recheck: python3 corpus/instruments/source-recheck.py --manifest
   corpus/source-snapshots/round-23/manifest.json --source S0xx`
   (`multiparty-vulnerability-coordination.md:4`,
   `cna-assignment-and-vulnerability-rules.md:4`,
   `cra-manufacturer-reporting-duties.md:4`). `find` shows only
   `S018.txt`/`S029.txt`/`S030.txt` under `source-snapshots/round-23/` — no
   `manifest.json`. `load_manifest` emits `UNAVAILABLE reason=missing`, exit 2
   (source-recheck.py:42-44). Fail-closed is correct behavior, but until the
   manifest lands, the "executable local recheck" has never produced a passing
   verification — Q7's "its successful output names what was checked" is
   undemonstrated. (In-flight deliverable; flagged so closure gates on it.)

8. **Two digest authorities, no cross-assertion.** `.ufo/waves/round-23/
   opened-source-snapshots.json` pins sha256 per S0xx; the future manifest will
   pin `sha256` again (source-recheck.py:77-80). Nothing asserts they agree.
   **Smallest correction:** one authority, or a manifest field/CI line
   asserting equality with the wave artifact.

9. **Manifest quote coverage vs entry Q3 rows is unbound.** Each entry's
   located-quote table is Q3 evidence; `source-recheck.py` verifies only the
   `quotes[]` assertions in the manifest (source-recheck.py:82-97, 127-133). If
   the manifest omits any entry quote row, that quote is verified by nobody —
   silently.
   **Falsifier:** drop one `quotes[]` assertion; entry still reads admitted,
   recheck still exits 0.
   **Smallest correction:** manifest assertions keyed to every located-quote
   row id in each entry; absence = exit 1.

10. **Snapshot↔official-text gap is disclosed but unverifiable.** `kind:
    "normalized public-doc reader excerpt; not raw HTTP bytes"`
    (opened-source-snapshots.json:7,15,23; lesson line 47-48 repeats it). A
    local recheck can never re-derive the snapshot from the URL; the chain
    rests on the 2026-10-20 opening event. Honest disclosure, residual trust,
    within Q7's letter — but C2's "independently verifiable" reduces to
    "quote-in-snapshot," and the claim should not imply more. Also note S029
    covers Articles 14/15/16/71 in one 19,900-byte excerpt — "official text
    opens" is satisfied at excerpt granularity, disclosed.

11. **"Current" CNA rules is a dated claim.** S030 = v4.2.0, effective
    2026-08-25 (S030.txt:12; lesson gate row:37). Verifiable only
    as-of-2026-10-20; the S022 (v4.1.0) → S030 supersession follows R8
    correctly (SOURCES.md:28,36) and F07's row should cite S030, not the queued
    S022 — the working-tree README rows F06–F08 are still `queued`
    (README.md:200-202), consistent with mid-flight state.

## Independence verdict

- C1 needs no frontier content; C2 needs no resolver change — disjoint
  production surfaces, as claimed (scorecard r23 §"independently measurable").
- Real couplings that break naive independent verification:
  (a) C2's new corpus `.md` files enter C1's census inputs → guard conflation
      (finding 6);
  (b) `corpus/lessons/round-23.md` and `corpus/QUALITY.md` are shared evidence
      files for both claims (single integration owner mitigates);
  (c) C2's `source:` header lines carry raw URLs in prose (not backticks — no
      new resolver tokens observed).

## Scope limits

No code executed per contract; all verdicts are static reads. Worktree is
mid-landing (untracked entries/snapshots/recheck script present; README F06–F08
still `queued`; manifest absent) — findings 7-9 are provisional on what L1
integrates. Denominator questions (8/8 vs r22's proposed (20+5)/25) are
CoverageDenom's seat; noted only where they touch the count command's
ambiguity. Fixture-safety and manifest-declarativity seats own their lanes.
