- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 38, base `a173b0c2`): the Gates & probes registry gains one EOF-appended row
      for `r38-closure.sh` — single line, 1446 B, sha256 `502bd887…`
      (`.ufo/waves/round-38/wave1/ScribeSkillRegistry.row.md`) — in the r37 row's column shape with
      net field count equal to the header's, `anchorcheck.py` exit 0 on the appended copy
      (`ScribeSkillRegistry.md` §2–§4). No-harm measured on a scratch mirror of `SKILL.md` + that
      row: `density.py` mean **233.1** (base 229.1; 27 blocks in both, path-citation instances
      760→768, only block 27 moves: 31→44 ev, 442.9→550.0 dens) and `anchorcheck.py` `16 in-range
      cite instances, 0 bad`, `LOST-RECORDED=306 PIN-BROKEN=0`, exit 0 (this seat, §Measurement; the
      base limb reproduces `ExecDensity.md` §1–§2 at 229.1 / 760 cites). The landed `SKILL.md` line
      number and digest are `[L1-MEASURE]`. Box stays `[~]`; no non-author check.

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 38): **no new end-to-end domain task ran this round.** The wave spec
      `.ufo/waves/round-38/wave1-spec.json` dispatches 73 seats, none of them a hunt-to-claim task
      (executor 21, scribe 15, reviewer 11, critic 7, mutation-tester 6, scout 6, connector 3,
      sentinel 2, simplifier 2), and `LOG.md` carried no `## Round 38` heading at base (1692 lines,
      newest `## Round 37` at :1678). The round-38 entry
      (`.ufo/waves/round-38/wave1/ScribeLOG.block.md`, appended at `[L1-MEASURE]`) logs the claims,
      both instruments and the F21 admission — not a domain hunt. The closest executed end-to-end
      work is measurement: the F21 capture committed at
      `corpus/source-snapshots/round-38/S055.txt` with its manifest (HTTP status 200,
      2026-10-26T18:25:51Z, 414858 fetched bytes, 272441 snapshot bytes / 5146 lines, sha256
      `63c8ad52…`, `.ufo/waves/round-38/wave1/ExecC2Capture.manifest.json`) and the round-38 suite's
      own run. Box stays `[~]`.

- [~] Instructions executable by an agent without oral context
      — evidence (round 38, base `a173b0c2`): the counters run from committed bytes with no oral
      context, each quoted with the result the frozen contract expects (all measured values at the
      round-38 head are `[L1-MEASURE]`): `bash corpus/instruments/r38-closure.sh --export-ref
      "$(sed -n 's/^export-ref=//p' .ufo/waves/round-38/final-gates/all-gates.txt)"` →
      `closed=8/8 exit=0`; the same substitution under `--selftest` → `selftest cases=8 failures=0`,
      one `selftest case=G<n>` line per check, and a plain run refuses with exit 2; the base
      `a173b0c2` export is the suite's own red control, `closed<8/8 exit=1`; the head is named by
      reference — judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt — and the
      committed transcript for both runs is that receipt. C2 counters:
      `python3 corpus/instruments/frontier-recheck-count.py` → `entries=24 pass=24 exit=0` incl.
      `PASS F21 ids=S055`; `python3 corpus/instruments/recheck-audit.py --quiet` →
      `expected=50 missing=0 unexpected=0 exit=0`; `python3
      corpus/instruments/capture-binding-check.py` → `records=45 bound=45 unbound=0`; `bash
      /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
      /home/vgpnk/Projects/shokunin kasegi` → exit 0 with only W04 S028/S029. Base limbs this seat
      measured: harness `entries=23 pass=23 exit=0`, audit `expected=49 … exit=0`, knowledge 49
      entries, 54 registry rows, frontier 20 rows. Box stays `[~]`.

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 38, base `a173b0c2`): `PROVINCE.md` (152 lines) and `corpus/README.md` (454
      lines) each carry an appended `Correction (round 38)` line naming the round-37 append as
      misplaced receipt scaffolding — PROVINCE L79-L152 (intended 2-line amendment at L79-L80,
      sha256 `cdfe44e3…`) and README L399-L454 (intended 27 lines, sha256 `2ebd8cd2…`; both digests
      recomputed in `ExecDeclaredBlocks.md` §5) — and the README block closes the fence left open at
      L426. `PROVINCE.md` gains the `[r38 Frontier amendment …] F21 —` line and README the
      `## Round-38 admission` paragraph, taking the frontier from 20 rows at base to 21 at the head
      (`[L1-MEASURE]`). Fence state at EOF is closed on both (this seat's walk: base PROVINCE
      `closed`, base README `open`; both `closed` with the round-38 blocks appended), and the
      appended blocks are declared in `.ufo/waves/round-38/declared-blocks.txt` (`[L1-MEASURE]` for
      their digests and the end state); the head is named by reference —
      judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt.
      F21/S055 ground is otherwise uncontested per the connector ruling
      (`.ufo/waves/round-38/wave1/ConnSibling.md`; the sweep in `ScoutF21Sibling.md` finds no
      CSAF/VEX/`product_status`/`known_not_affected` ground in any sibling lane or the merge).
      kake's `CSAF` mention
      (`kake-shokunin/corpus/knowledge/security-txt-publishing.md:63`) names it only as a
      security.txt extension field — adjacent, reported, not absorbed. Box stays `[~]`.
