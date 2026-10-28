VERDICT: BROKEN

Scope: control-adequacy review of `.ufo/waves/round-45/controls/freeze-controls.py` / `freeze-controls.txt`, and falsification of the frozen counters `corpus/instruments/r45-routed-defects.py` (C1) and `corpus/instruments/r45-c2-gate.py` (C2) at freeze commit 8cf62c8 (lane HEAD 5242db6 leaves those files unchanged; `git diff --stat 8cf62c8 HEAD` over counters, claims and controls prints nothing). Base export: `git archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`, diffed identical to the L1 pure export. All fixtures were built in scratch and removed on exit. Nothing was committed, staged or fetched live.

Re-run of the frozen control receipt (reproduces exactly):

    $ python3 .ufo/waves/round-45/controls/freeze-controls.py --base-export $SCR/base --lane $LANE --work $SCR/work
    control do-nothing-base counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
    control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1 expect=RED got=RED
    control c1-marker-only counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
    control c2-junk-row counter=C2 c2-gate fixed=4/7 exit=1 expect=RED got=RED
    control c2-fabricated-quote counter=C2 c2-gate fixed=5/7 exit=1 expect=RED got=RED
    controls total=5 red=5 green=0

The five controls discriminate against do-nothing and against marker prose. They do not test any tree that puts a token-echo stub or hand-typed text where a check runs. Findings follow.

## F1 — C1 counter is satisfiable by a cheap stub tree (kill-rule breach)

Attacked: `r45-routed-defects.py` limbs R1-R5 against a tree I built (`build.py` `c1_stub_echo`). The tree adds one honest-looking S072 registry row (sha256 pinned to the frozen S072.txt, `supersedes S070 —`, `rejected`, `flip:`, `10029`, `readable`), the round-44 `Correction (round 45` line, R47/R48/R49 rows whose `enforced-by:` names the existing `corpus/instruments/r44-frontier-count.py`, a `--selftest` echo in that probe that prints `selftest cases=8 failures=0`, a `freeze-check.py` that prints `selftest cases=6 failures=0` and `freeze-check claims=2 base_ok=2` with no logic, a hand-typed refiled receipt, and the frozen claims.json copied in.

Command and output:

    $ python3 $LANE/corpus/instruments/r45-routed-defects.py --root $SCR/t/c1-stub-echo --baseline $SCR/base
    limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
    limb R2 fixed=1 read=criteria=3
    limb R3 fixed=1 read=selftest-cases=8
    limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2
    limb R5 fixed=1 read=refiled=ok original=unchanged
    routed-defects total=5 fixed=5 unresolved=0 exit=0

Grade 5/5 GREEN, which the C1 kill rule forbids for any control and which the counter's own predicate ("five limbs R1-R5 resolved") is meant to reject. Discriminated against do-nothing (`limb R3 fixed=0 read=selftest-rc=2-tokens=None`, `limb R4 fixed=0 read=freeze-check-absent`) and against marker-only, so the counter is not measuring the claimed work for R2-R5.

Per-limb reasons it passes:

- R2: `enforced-by` only requires an existing path; the counter does not require the path to be a round-45 artifact. The stub cites a pre-existing file.
- R3: the counter only parses the `selftest cases=N failures=0` token printed by a probe that I patched to echo it. Nothing runs the probe's cases.
- R4: the counter only parses the replay token. It does not check that `freeze-check.py` reads its `--claims` argument, and it does not require the claims file to exist: with `.ufo/waves/round-45/claims.json` removed from the tree, the same counter still prints `limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2` and `routed-defects total=5 fixed=5 unresolved=0 exit=0`.
- R5: the counter checks text in the receipt. I typed that receipt by hand; nothing was executed to produce it, and R5 grades it GREEN.
- R1: text-only. Its `10029` token is in fact correct against the raw capture (checked: `source-recon/S072.json` body `len(json.load(...)['body'])` = 10029), but the counter never checks it, and the `flip:` clause is not evaluated.

Cheapest-adversary answer: the marker-only tree is not the cheapest tree an adversary would try. The echo-stub tree above costs about the same as marker-only (one registry row, two stubs, copied frozen snapshots and claims) and grades 5/5 GREEN. The C1 control set should therefore add `c1-stub-echo` (expected RED) before any seat scores.

## F2 — Repairs tested in scratch (not committed)

Two repairs to the C1 counter, run on the same stub tree and the base:

- R2': `enforced-by` path must exist in the tree and must not exist in the base (a round-45 artifact).
- R4': the frozen replay must also reject a planted mutant claims file (the same bytes plus one trailing space) — the real freeze-check must refuse it; a stub that prints `base_ok=2` regardless does not.

Output:

    $ python3 $SCR/repair/r45-routed-defects.py --root $SCR/t/c1-stub-echo --baseline $SCR/base
    limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
    limb R2 fixed=0 read=R47-enforced-by-predates-round-45-corpus/instruments/r44-frontier-count.py
    limb R3 fixed=1 read=selftest-cases=8
    limb R4 fixed=0 read=mutant-claims-accepted-rc=0
    limb R5 fixed=1 read=refiled=ok original=unchanged
    routed-defects total=5 fixed=3 unresolved=2 exit=1

The repaired counter on do-nothing base stays at `fixed=0 ... exit=1` (`limb R4 fixed=0 read=freeze-check-absent`), so the repair does not weaken the control. Not fixed by these repairs: R3 (the probe's echo selftest is still accepted), R5 (hand-typed receipt still accepted), and the absence of any real `freeze-check.py` implementation (no real R4 green path exists yet). A real R3/R5 check would have to re-run the probe and the receipt's command; I did not build that.

## F3 — C2 junk-row control and its stronger variants

Built on the base export plus one F27 row, one knowledge entry, and optionally a SOURCES S071 row and the frozen snapshot/manifest. Entry quotes are real text cited at the spans I located in `S071.txt` (`20-21`, `39-40`, `41-43`, `95-96`, `310-311`).

Command: `python3 $LANE/corpus/instruments/r45-c2-gate.py --root <tree>`

- c2-honest-draft (positive control; the counter must be satisfiable):

      gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-process.md
      gate G2 pass=1 read=source=1 verified-at=1 recheck=1
      gate G3 pass=1 read=row-S071=ok
      gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
      gate G5 pass=1 read=spans=5 located=5 failed=0 cores=4/4
      gate G6 pass=1 read=knowledge=64
      gate G7 pass=1 read=census-rc=0
      c2-gate fixed=7/7 exit=0

- c2-real-no-registry (real entry and quotes, no SOURCES S071 row): `gate G3 pass=0 read=row-S071=absent-or-malformed` … `c2-gate fixed=6/7 exit=1`. RED, correct.
- c2-registry-no-snapshot (SOURCES row kept, snapshot and manifest removed): `gate G3 pass=0 read=snapshot-absent`, `gate G4 pass=0 read=manifest-absent`, `gate G5 pass=0 read=spans=5 located=0 failed=5 cores=0/4`, `c2-gate fixed=4/7 exit=1`. RED, correct.
- c2-whole-file-cite (identical to the honest draft, but every quote cites `S071.txt:1-372`): `gate G5 pass=1 read=spans=5 located=5 failed=0 cores=4/4`, `c2-gate fixed=7/7 exit=0`. GREEN. G5 checks substring location in the cited window only, not that the window is the quote's own lines, so a whole-file citation makes the locate check vacuous.
- c2-consistent-forgery (a sentence not in the source — `Embargoes last up to 7 calendar days for every reporter, with no exception.` — appended to S071.txt as line 373; manifest sha256/bytes/lines and the SOURCES anchor re-pinned to the forged bytes; entry quotes it at `S071.txt:373`): `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`, `gate G5 pass=1 read=spans=6 located=6 failed=0 cores=4/4`, `c2-gate fixed=7/7 exit=0`. GREEN. Diff against the lane snapshot shows only the appended line (`372a373`).

Pin check against the frozen commit (read-only):

    $ git grep -l 0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40 8cf62c879e6e6b031e67412f8fac1fba0bd378cf -- .
    8cf62c879e6e6b031e67412f8fac1fba0bd378cf:corpus/source-snapshots/round-45/manifest.json

The only independent-looking pin of the S071 sha is the manifest itself. `freeze.txt` pins only `claims-sha256`, and `claims.json` names the snapshot path with no digest. So a consistent forgery of the snapshot, manifest and anchor passes G3-G5. Only a procedural non-author re-fetch (kill rule text) catches it; the counter cannot.

Repairs tested in scratch: G5 requires the cited span to be at most three lines wide (`b - a > 2` is a failure); G4 requires the snapshot sha256 to equal the value pinned in the freeze commit (`0918dcfa…`, which equals `sha256sum` of the frozen S071.txt). Output:

    $ python3 $SCR/repair/r45-c2-gate.py --root $SCR/t/c2-whole-file-cite
    gate G5 pass=0 read=spans=5 located=0 failed=5 cores=0/4
    c2-gate fixed=6/7 exit=1
    $ python3 $SCR/repair/r45-c2-gate.py --root $SCR/t/c2-consistent-forgery
    gate G4 pass=0 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
    c2-gate fixed=6/7 exit=1
    $ python3 $SCR/repair/r45-c2-gate.py --root $SCR/t/c2-honest-draft
    c2-gate fixed=7/7 exit=0
    $ python3 $SCR/repair/r45-c2-gate.py --root $SCR/base
    c2-gate fixed=1/7 exit=1   (do-nothing)

The honest draft stays 7/7 under the repaired counter, so the repairs do not make the target unreachable. The repairs do require a freeze-record pin line, which is not in the frozen commit; adding it is a freeze change the L1 must decide.

## F4 — Other limits of the C2 counter

- G7 runs `CENSUS` at the default fleet path `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, outside the lane and outside the freeze commit. The counter's G7 result therefore depends on a fleet file that is not frozen (`SOURCES_CENSUS` env override exists; the controls did not set it).
- G6 is an exact count (`knowledge/*.md` == 64) and reads no file content: any 64-file tree passes it, whatever the files say. In the junk-row control the 64th file is the junk entry, so G6 is satisfied by the junk file alone.
- G2 checks the `recheck:` line by length only (`len(h) > 10`).
- G5 accepts any span up to 25 words; the frozen core checks only require each core to appear inside some located span, not in the entry's own citation.

## Control-set adequacy (answers to the seat questions)

- Do the frozen controls really skip the claimed work? do-nothing base: yes (absent artifacts). marker-only: yes for R1-R5 artifacts (no S072 row, no freeze-check, no real correction tie); it appends a `Correction` line and a `nothing.py` path that does not exist, so R2 fails for the right reason. junk-row: yes (no SOURCES row, no snapshot). fabricated-quote: yes (quote absent from the snapshot). None of the five tests stubs or hand-typed receipts, which is where the counters fail.
- Is marker-only the cheapest tree? No. `c1-stub-echo` (F1) costs about the same and grades 5/5 GREEN.
- Is the C2 junk-row control missing a stronger variant? Yes: consistent forgery and whole-file citation (F3) both grade 7/7 GREEN. The real-no-registry and registry-no-snapshot variants are RED as the counter should be.

## Recommendations to the L1 (not applied)

1. Add `c1-stub-echo` and `c2-whole-file-cite`, `c2-consistent-forgery` to `freeze-controls.txt` as controls expected RED before any seat scores, and extend `freeze-controls.py` to build them.
2. Repair C1 R2 (enforced-by must be a round-45 artifact), R4 (mutant-claims rejection and claims-file existence), and address R3/R5 (re-run the probe and receipt command; do not accept a typed receipt). Repaired code is in scratch only.
3. Repair C2 G5 (span width ≤ 2) and G4 (freeze-record sha pin for S071.txt). Both need the L1 to decide on a freeze change.
4. Keep the honest-draft positive control in the suite so the repaired counters are shown to be satisfiable.

## Limitations

- No live fetch of docs.kernel.org or bughunters; S071/S072 provenance is taken from the frozen snapshots and `source-recon` files as committed.
- The honest draft is my own fixture built from the frozen snapshot and manifest, not a builder's deliverable. It proves the counter can go GREEN, not that a builder produced the entry.
- The repaired counters are scratch copies with minimal patches; they were run once each, deterministic, and are not a committed fix.
- No real `freeze-check.py` exists (absent at base and at freeze), so no green R4 path was exercised.
- Single run per tree; the counter outputs are deterministic over the trees.
- Scratch `$SCR` (`/fast/scratch/hyaku/kasegi-r45/R45RevControls`) removed on exit. `git status --short` after the work shows only the four pre-existing untracked entries (`final-attempt3-refiled.txt`, `wave1.ready`, `wave1.ready.dispatched`, `wave1/`); no tracked file changed.
- Installed tools: none.
