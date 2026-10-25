# ExecReceiptCanonC1 — canonical C1 receipt-index draft (round 28, wave 1)

Seat: executor, leaf, read-only. No production file touched. No VCS write, no subagent, no background job,
no tool install. All artifacts under `.ufo/waves/round-28/`.

## Deliverable

`.ufo/waves/round-28/receipts/ExecReceiptCanonC1.txt` — the exact content the L1 should write to
`.ufo/waves/round-28/c1-receipt-index.txt` at close, as a BEGIN/END-delimited block, every value line
labelled with its source receipt path. **No canonical file was created** (defect 4).

## Values collected (all at the landed instrument digest)

Instrument sha256 `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514` — the same digest
ExecImplC1's receipt declares; digest equal before/after every run (`STABLE_DURING_BATCH=yes`).

| counter | value | source |
|---|---|---|
| (a) bad-fixture | `BASE-ABSENT=1` printed, `exit=1` | final-batch.log; ExecImplC1.txt:36-37 |
| (b) bounties-fixture | `BOUNTIES-ABSENT_lines=1`, `exit=1` | final-batch.log; ExecImplC1.txt:40-47 |
| (c) `--selftest` | `selftest cases=9 failures=0`, `exit=0`, deterministic (run twice) | final.selftest1/2.out |
| (d) SKILL.md | `exit=0`, `0 bad`, `LOST-RECORDED=306`, classes unchanged | skill.final.out |
| disclosure | `0` newly LOST-RECORDED (0 per each of the 4 files); corpus BOUNTIES-ABSENT total `0` | final-batch.log; claims-erratum-1.md |

Frozen counter-(c) greps were executed against the filled block: `grep -cE 'selftest cases='` → `1`;
digest token → one line, equal to `sha256sum`.

## Stability method (why the numbers are not mutable-byte readings)

The instrument changed 14 times during collection. A 5 s digest probe gated every recording on: digest held
still (5 consecutive samples) AND all four after-values reached. A mid-flight sample at `29aba084…` is
retained as evidence that a partial file reaches (a)/(b) while `--selftest` raises
`NameError: name '_selftest' is not defined` — i.e. the four limbs are genuinely independent.

## Findings reported to the L1 (none fixed by this seat — not my files)

- **F-A**: frozen counter (d)'s `bad=` sed is vacuous (`bad; N bad` vs grammar `N bad; K distinct anchors`).
  bad=0 is measurable via `grep -oE '[0-9]+ bad;'`. Corroborated by ExecImplC1 "O1".
- **F-B**: the frozen `corpus_disclosure` cell ("4 … newly LOST-RECORDED") measures **0 of 4**. The 4 cites
  are plain-text `source:` trailers, outside the backtick-only `TOK`; lane-wide backticked anchored bounties
  tokens = 0. Proven with a CITE-arm-only scratch patch (+63 bytes) and on landed bytes. Already reconciled
  by `.ufo/waves/round-28/claims-erratum-1.md`.
- **F-C**: SKILL.md is not byte-identical to the before-capture — one line moved (`md:998`→`md:999`) from
  ScribeSkillGate's registry row at line 980. Class counts and summary unchanged, so C1(d) holds, but
  byte-identity must not be claimed.
- **F-D**: `assemble-receipts.py` reads the SKILL.md line as the last output line (a verdict line, not the
  summary). The drafted block selects `^== SKILL.md:` and is immune.

## Risks / blockers

No blocker. Residual risk: the instrument can still move after `17:29:56Z`; the receipt's §6 gives the
staleness gate (digest must equal `95333e29…` at assembly) and the exact re-run set if it does not.
