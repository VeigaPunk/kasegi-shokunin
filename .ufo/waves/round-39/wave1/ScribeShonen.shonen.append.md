- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 39, base `480b1a50`): the Gates & probes registry gains one EOF-appended row
      for `r39-closure.sh` — appended, nothing rewritten, so at the landed head `git diff --numstat
      480b1a505a2dfc14a4f718d16d63808247214d0a -- SKILL.md` shows a zero deletion count; the append
      is the L1's integration step (no wave-1 seat drafts that row) and its landed line number and
      digest are `[L1-MEASURE]`. The base limb is measured, not inferred: `SKILL.md` 1114 lines,
      sha256 `0937bce5…`, `anchorcheck.py SKILL.md` exit 0 (`16 in-range cite instances, 0 bad;
      16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`)
      and `density.py SKILL.md` mean **233.1** over 27 blocks, 768 path-citation instances — this
      seat's runs, reproduced in `.ufo/waves/round-39/wave1/ExecArchiveChecks.base-gates.txt`. Box
      stays `[~]`; no non-author check.

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 39): **no new end-to-end domain task ran this round.** The wave spec
      `.ufo/waves/round-39/wave1-spec.json` dispatches 49 seats — executor 27, scribe 11, reviewer 6,
      scout 2, critic 2, connector 1 — and none is a hunt-to-claim seat; `LOG.md` carried no
      `## Round 39` heading at base (1702 lines, newest `## Round 38` at :1694). The closest executed
      end-to-end work is measurement: the F22 capture `corpus/source-snapshots/round-39/S057.txt`
      (275 lines, 17971 bytes, sha256 `11c8d6d6…`) with its manifest — HTTP 200 at
      2026-10-26T19:30:55Z, 235270 fetched PDF bytes, landing page 54453 raw bytes sha256
      `4e6aa483…`, quotes Q1-Q4 anchored at capture L12-L14, L132-L134, L136-L138 and L184-L186
      (`.ufo/waves/round-39/wave1/ExecFrontierCapture.manifest.json`) — plus the F22 harness
      admission (`PASS F22 ids=S057`, `entries=25 pass=25 exit=0` on the composed after-mirror,
      `.ufo/waves/round-39/wave1/ExecHarnessProbe.harness.txt`) and the round-39 suite's own run.
      Box stays `[~]`.

- [~] Instructions executable by an agent without oral context
      — evidence (round 39, base `480b1a50`): the counters run from committed bytes with no oral
      context. Suite: `bash corpus/instruments/r39-closure.sh --export-ref "$(sed -n
      's/^export-ref=//p' .ufo/waves/round-39/final-gates/all-gates.txt)"` → `closed=8/8 exit=0`;
      `--selftest` under the same substitution → `selftest cases=8 failures=0` with eight graded
      `selftest case=G<n> … positive=pass … verdict=pass` lines; a plain run refuses with exit 2 (this
      seat: `bash -n` clean, plain run `exit=2`); the base export `480b1a50…` and the round-38 closure
      head (`66703aca…`) are the suite's own red controls, `closed=2/8 exit=1` (§2.3-2.4 of
      `.ufo/waves/round-39/wave1/ExecSuiteBuild.md`), and the same suite is green on a scratch overlay
      head carrying the round's evidence — `closed=8/8 exit=0`, `selftest cases=8 failures=0`, eight
      graded case lines (§2.7), while the base selftest is honestly red at `cases=8 failures=6`
      (§2.6); a run at the judged head itself prints `closed=7/8 exit=1` with `G2 … receipt=0`,
      documented per claims erratum 1 E4, and the run at the verification ref Y stays `[L1-MEASURE]`
      until `final-gates/all-gates.txt` is filed. The round-39 head is named by reference only —
      judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt — and the committed
      transcript for both runs is that receipt. C2 on the composed after-mirror:
      `capture-binding-check.py` → `records=46 bound=46 unbound=0`; `recheck-audit.py --quiet` →
      `expected=51 missing=0 unexpected=0 exit=0`, `strict pass=51/51`; `source-recheck.py
      --manifest corpus/source-snapshots/round-39/manifest.json --source S057` → `S057:sha256 OK`
      with Q1-Q4 `OK` and exit 0 (`.ufo/waves/round-39/wave1/ScribeEntryF22.md`);
      `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0 with only
      W04 S028/S029; knowledge 50 → 51,
      frontier 21 → 22 (`.ufo/waves/round-39/wave1/ExecCensusAfterMirror.mirror-metrics.txt`; the
      integrated-tree re-runs are `[L1-MEASURE]`). Base limbs this seat measured: harness
      `entries=24 pass=24`, audit `expected=50 … exit=0`, binding `records=45 bound=45`, knowledge 50
      entries, 55 registry rows, frontier 21 rows. Box stays `[~]`.

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 39, base `480b1a50`): `PROVINCE.md` gains the round-39 end-of-file amendment
      `[r39 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F22 — CISA When to
      Issue VEX Information …` — one line, 262 B with its LF, sha256 `bd8dbc09…`
      (`.ufo/waves/round-39/wave1/ScribeProvinceF22.province.append.md`; landed line number is
      `[L1-MEASURE]`, 156 base lines + 1) — and `corpus/README.md` (486 base lines, paired fences at
      EOF) gains the 28-line `## Round-39 admission` block, 2085 B, sha256 `a8aa90a2…`
      (`.ufo/waves/round-39/wave1/ScribeFrontierF22.readme.append.md`), which opens no fence and
      states the frontier at **22/22 admitted** (21 rows at base). No sibling lane and no shokuknow
      merge row holds the issuance/lifecycle/reaffirmation/inheritance ground — 20 lane roots
      (829,134 files) and the shokuknow tree (24,415 files) swept with zero `When to Issue`, `VEX`,
      `exploitability exchange`, `OpenVEX` or `CycloneDX` hits, kake's `CSAF` extension mention
      adjacent and unabsorbed (`.ufo/waves/round-39/wave1/ScoutSiblingF22.sibling.md`) — and the
      fabricated twin `.ufo/waves/round-39/c2-controls/junk-f22.md` is rejected: `source-recheck.py`
      returns `MISMATCH reason=quote-not-found` for J1-J4 and exit 1, while the positive and
      isolation controls over the same capture exit 0
      (`.ufo/waves/round-39/wave1/ExecJunkRecheck.junk-recheck.txt`). Box stays `[~]`.
