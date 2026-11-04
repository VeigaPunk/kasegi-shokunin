# Round 67 — multi-head SIGPIPE input-completeness (DRAFT, predata)

**Status: DRAFT by seat ScribeRound. Not landed. No production byte was created or modified by
this seat; no commit, push, publish or deploy; no git index or jj state touched. The L1 is the
sole production integrator.**

Drafted from the round-67 wave's own evidence only, in the shape of `corpus/lessons/round-66.md`.
Every cell that cannot be sourced from a wave receipt is marked **pending L1 integration** rather
than invented. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`; production gate under test
`corpus/instruments/figure-audit.py` sha256
`51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac` (re-verified by this seat
after the wave began — unchanged from base).

One intended C1 (depth:verifiability, lowest, nominal 4 held under R58) and one intended C2
(coverage, 8 held). This predata lesson does **not** freeze a predicate or a counter.

## Gate

**G1 — the round-67 own-work diagnostic (C1).** Opened 2026-11-04. Production
`corpus/instruments/figure-audit.py` at base `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`,
sha256 `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac`. Located quotes, with
word counts:

- L120 `if os.path.basename(head) != "cat":` (7 whitespace-delimited words) — the head-blind
  exemption: every **non-cat** head keeps SIGPIPE benign.
- L113 `SIGPIPE is stale: the truncation can hide a later operand's error.  Other heads keep the` (14 words)
- L122 `return not cat_sigpipe_exempt(stage_argv)` (5 words)
- L39 `or a non-exempt upstream signal — SIGPIPE from a multi-input or option-carrying cat is stale —` (14 words)

Admit the base gate and the round-67 controls as an own-work source **only** for this local
diagnostic: an early consumer can kill a streaming read-only head before it reaches a later named
operand, so surviving output does not establish that all named inputs were read. Reject the
reading that a SIGPIPE'd non-cat head proves input completeness, and reject any sandbox,
source-restoration, arbitrary-wrapper, pipefail or general shell-correctness guarantee. This is
source curation for a local diagnostic, **not** a knowledge or frontier admission.

**G2 — the round-67 no-work control (C1).** Opened 2026-11-04:
`.ufo/waves/round-67/controls/donothing-multihead-r67.py` and its receipt
`.ufo/waves/round-67/controls/donothing-multihead-r67.txt` (L1-authored, committed in the wave
root). Located quotes from the receipt:

- L3 `NATIVE P9 stages=[-13, 0] derive=cut -f1 -d: big.txt missing.txt | head -n 1`
- L11 `FIG P10 recorded=4096 big.txt derived=4096 big.txt ok`
- L19 `NOWORK-VERDICT gate=corpus/instruments/figure-audit.py green_on_masked=P9,P10,P11,P12,P13,P14`

The base gate reads `ok` on three two-operand shapes whose second operand was never opened
(`cut`, `wc`, `grep`), while the single-input controls `cut`/`wc`/`sha256sum` also read `ok` and
`head -n 5 big.txt missing.txt` reads `derive-upstream-exit-1 stale` (upstream exit 1).
**The P10 (`wc`) line is not stable** — see M67-2.

**G3 — the L1 flakiness correction (C1).** Opened 2026-11-04:
`.ufo/waves/round-67/controls/dispatch-addendum-r67.md`. Located quote: `MEASURED FACT: \`wc -l
big.txt missing.txt | head -n 1\` (P10) is FLAKY at native level on this host.` The addendum
requires that P10 not be frozen to one reason and that the candidate read stale for P10 under
both outcomes; the frozen repair set is **cut (P9)** and **grep (P11)**. Receipts cited by the
addendum: `.ufo/waves/round-67/controls/native-statuses-r67.txt` (one pass, P10 = 1) and the L1
repeat probe (five passes, P10 = -13).

**G3b — the candidate gate and its falsification battery (C1).** Opened 2026-11-04:
`w1/ExecMultiHeadGate.md` (candidate sha256
`978c98a2c35dbd16ad66475bdd966f9ed73d17b4c642ae8210287a7345fa3a36`) and
`w1/ExecMultiHeadProbes.md` (harness `w1/ExecMultiHeadProbes/probes.py`, CLI
`--instrument PATH --work DIR --mode base|candidate`). Located quotes:

- `PROBES probes=18 failures=3 mode=candidate`, exit 1 — "failures exactly P9, P10, P11" (the
  candidate-vs-base delta at the base gate).
- `Base run: probes=18 failures=0, exit 0.` (the production base conforms to the derived matrix on
  every shape, including r66's cat carve-out).
- `cases=71 failures=0` (candidate selftest) and `cases=71 failures=3, exit 1` for the
  base-graft falsification copy.
- `PAYLOAD-DEV base P1,P2 payload=rc0 frozen=rc1/derive-upstream-signal-13` — the base already
  carries r66's `cat_sigpipe_exempt` restriction; the payload's base text predates it.
- `PAYLOAD-DEV candidate P8 payload=rc1/derive-upstream-signal-13 frozen=rc0` — `grep -c` emits one
  2-byte write at EOF, so it never SIGPIPEs; P18 was added as the streaming-grep positive control.

**G3c — the sentinel's security review of the candidate (C1).** Opened 2026-11-04:
`w1/SentinelMultiHead.md`. Located quotes:

- `Verdict: FINDINGS — F1 (Low, pre-existing masking not closed by the rule), F2 (Informational,
  test-strength). No widening, no newly admitted head or flag, no new write path, no production
  regression.`
- `MATRIX derives=96 diffs=0` — a 96-derive admission parity matrix shows the change admits
  nothing new.
- `widened=0 narrowed=10 identical=42` — a 52-derive differential sweep; the conservative direction
  is monotone.
- `sigpipe_input_count("wc", ["wc","--","-x","missing.txt"]) = 1` and
  `sigpipe_input_count("cut", ["cut","-f1","--","-x","missing.txt"]) = 1` — the sentinel's
  independent statement of the mid-`--` residual (see M67-9).
- `the change's own stated contract ("SIGPIPE is exempt only when the decoded argv names at most
  one input operand") is not met, so C1's closure claim must be scoped to plain multi-operand forms.`
- `r66 frozen receipts reproduce: round-66 probes.py --mode candidate on this candidate →
  PROBES probes=8 failures=0`.
- `Production ledger …: candidate figures=35 ok=35 stale=0 exit=0, base identical`.

**G3d — the mutation battery (C1).** Opened 2026-11-04: `w1/MutationMultiHead.md` and
`w1/MutationMultiHead/multihead-mutbat.py` (sha256 `937f8677…`, 17582 B), run against the
candidate `d5e8fcae…`. Located quotes: `MUTBAT killed=7/7 survivors=0 equivalents=3
invalid_rejected=0 failures=0`, exit 0, and `two consecutive full runs produced identical verdict
lines`. Limb L4 is `drop-dashdash` (killed by `P11-dashdash-leading`); limbs L1/L2 are the grep
non-file-arg base; L3 the cat/cut/wc base; L5 count-options-as-operands; L6 unknown-head-stale;
L7 the head-blind rule itself. Equivalence controls: `E1-trailing-space-control`, `E2-le-one-vs-lt-two`,
`E3-sigpipe-constant`.

**G3e — the F45 novelty screen by the connector seat (C2).** Opened 2026-11-04:
`w1/ScopeF45/screen.md`. Located quotes:

- `Targets Scanned (205 files total)` … `Total hits across all surfaces: 59 hits.`
- `Decision: F45's ground is GENUINELY NEW (UNCOVERED).`
- `Zero held rows, zero knowledge entries, and zero source snapshots in kasegi-shokunin hold PSIRT
  maturity-level ground.`
- `S098 has grep -cE 'Maturity Level|Level [123]' = 0. It contains no maturity levels, no
  capability ladders, no self-assessment framework, and no level-specific checklists.`
- `Coverage Verdict: IN PROVINCE.` and `It is documentation only; live-target testing remains
  refused.`
- The four consumer-confusion pairs with narrowing sentences: F44 (horizontal catalogue vs vertical
  ladder), F10 (one vendor's public policy vs the community maturity model), F13 (bug-severity
  ladders vs team capability tiers), F43 (inter-organizational phase allocation vs
  intra-organizational maturity progression).

**G4 — RevengerMultiHead's native premise table (C1).** Opened 2026-11-04:
`.ufo/waves/round-67/w1/RevengerMultiHead.md` and `.ufo/waves/round-67/w1/RevengerMultiHead/table.txt`.
Located quotes:

- `wc` is the exception that contradicts the wording of the claim: it *does* reach the later
  operand — at every size its stderr names `missing.txt` and the strace shows
  `openat(missing.txt) = -1 ENOENT` — and then dies of `-13` on a later write of its own summary
  lines.
- `cut`/`grep`/`head -n <large>`/`tail -n +1` mask from ≈65–70 KiB, `cat` only above ≈512 KiB;
  the boundary is head-specific, not the 64 KiB pipe capacity.
- Base masking is **not** limited to `cut`/`wc`/`grep`: `head -n 100000 …` and `tail -n +1 …`
  are green on a world whose second operand was never opened.

**G5 — FIRST's PSIRT Maturity Document (C2), the round-65 lead.** Opened 2026-11-04 by this
seat, independently of ScoutF45. URL
`https://www.first.org/standards/frameworks/psirts/psirt_maturity_document`, HTTP 200,
`Last-Modified: Mon, 26 Jan 2026 14:43:46 GMT`. Captured with the lane instrument
`corpus/instruments/capture-source.py --kind html` into this seat's directory as
`w1/ScribeRound/F45-PSIRT-MATURITY.txt`: **478 lines, 59068 bytes, sha256
`cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f`**. The same snapshot digest
is recorded by the independent ScoutF45 capture (`w1/ScoutF45/S100.txt`, sha256 `cf834a65…`,
478 lines), so the two captures are byte-identical.

Located quotes (line number in the 478-line snapshot; word count in parentheses):

| # | anchor | quote | words |
|---|---|---|---|
| Q1 | L1 | `Product Security Incident Response Team (PSIRT) Maturity Document` | 8 |
| Q2 | L217 | `PSIRT Maturity Levels to demonstrate Operational Capability and Maturity` | 9 |
| Q3 | L218 | `Maturity Level 1 (Basic) - The Beginning is a very fine place to start` | 14 |
| Q4 | L221 | `These referenced use cases cover a spectrum of developmental levels from a newly-established PSIRT, through a more advanced Incident Response team` | 21 |
| Q5 | L221 | `The framework does not cover topics such as capacity - the number of vulnerabilities and incidents a team can manage simultaneously` | 21 |
| Q6 | L224 | `The use of the term "maturity" in this document is intended to describe a profile of a product security team` | 20 |
| Q7 | L285 | `Maturity Level 2 (Intermediate) - I am reactive, but I’ve trained for it!` | 13 |
| Q8 | L318 | `Maturity Level 3 (Advanced) - Proactive...we’re ready for anything (mostly)` | 10 |
| Q9 | L353 | `Beyond “Level 3”` | 3 |
| Q10 | L363 | `PSIRTs should have a defined charter that describes what the PSIRT does, and its scope.` | 15 |
| Q11 | L397 | `Annex 7: Sample Checklist` | 4 |

The document's own structure: a title (L1), a purpose line (L217), three named levels —
Level 1 Basic (L218), Level 2 Intermediate (L285), Level 3 Advanced (L318) — an explicit
"Beyond Level 3" (L353) and seven annexes, of which Annex 7 is a per-level **sample checklist**
(L397) grouped by service area (Operational Foundations / Stakeholder Ecosystem Management /
Vulnerability Discovery / Vulnerability Triage / Remediation / Vulnerability Disclosure / Training
& Education) for Level 1 (L398), Level 2 (L418) and Level 3 (L445). Measured on the capture:
`Maturity Level 1` ×4, `Maturity Level 2` ×3, `Maturity Level 3` ×3, `Beyond` ×1,
`self-assess` ×0. **The document carries no self-assessment or self-attestation mechanism**; the
checklist is a sample checklist, not a scored rubric. That is a limit to be recorded, not a
capability claim.

**G6 — the round-65 lead record for the same URL (C2).** Opened 2026-11-04:
`corpus/SOURCES.md:244`. Located quote: `Lead added (round 65, not admitted): FIRST PSIRT
Maturity document at https://www.first.org/standards/frameworks/psirts/psirt_maturity_document —
opened only for boundary screening this round (HTTP 200, 82978 bytes, sha256
`334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e`; text carries "Maturity
Level 1 (Basic)" through "Beyond Level 3").` and `A future admission needs its own source id,
manifest and entry; S098 states no maturity levels.` The lead was **never admitted**; no registry
row, no manifest, no knowledge entry exists for it at base.

**Novelty screen against F44 (G5/G6).** F44 is S098, the PSIRT Services Framework v1.1 service
catalogue (`corpus/README.md:1043`, `corpus/knowledge/first-psirt-services-framework.md`).
Measured on the S098 capture `corpus/source-snapshots/round-65/S098.txt`:
`grep -cE "Maturity Level|Level [123]"` → **0**; `Maturity Level` headings absent; the only
maturity *definition* is the glossary entry at S098 L1510 (`Maturity - how effectively an
organization executes a particular capability within the mission and authorities of the
organization.`) and the one measurement remark at L675 (`Maturity of a PSIRT may be measured via
the availability and efficiency of the difference services prescribed in this service area.`).
S098 links the maturity document only as a sidebar download at L1553 (`PSIRT Maturity, HTML`).
The held F44 entry already records this boundary explicitly:
`corpus/knowledge/first-psirt-services-framework.md:45` — `Maturity is a glossary definition, not
a level ladder.`
A term sweep over `corpus/knowledge/` finds **exactly one** file mentioning maturity
(`first-psirt-services-framework.md:45`, the boundary sentence itself); `capability level`,
`self-assessment` and `self assessment` find **zero** hits across `corpus/knowledge/`, `SKILL.md`
and `PROVINCE.md`. **F45's ground — a named three-level maturity ladder with a per-level service
checklist — is genuinely new against every held row and entry.** It is a different document from
S098, not an extension of it.

**G6b — the F44/F45 version boundary (C2), measured by this seat.** The maturity document is
**older** than the framework the corpus holds. Its companion PDF has
`CreationDate: Thu Dec 6 17:32:58 2018 -02` (29 pages) and its Annex 1 points at the **v1.0**
framework — verified in this seat's own capture at L356-L357:
`For a complete list of supporting resources and glossary refer to the PSIRT Services Framework`
/ `https://www.first.org/education/FIRST_PSIRT_Services_Framework_v1.0.pdf.` (also the only
occurrence of `Services_Framework_v1` in the PDF text layer). The corpus holds the **v1.1**
framework page as S098. **F45's level ladder is therefore keyed to the v1.0-era service
catalogue, not to S098's v1.1 page.** This is the cleanest statement of the F44/F45 boundary and
it is a limit the entry must carry: a F45 claim about "the service areas a level expects" is a
claim about the v1.0 catalogue, not about the v1.1 catalogue the lane holds under F44.

**G7 — the F45 digest-reproducibility finding (C2), measured by this seat.** The round-65 lead
records a **raw-body** digest for this URL. That digest is not re-derivable: the page carries a
per-response CSP nonce in its script tail, so the served HTML's bytes are constant in **length**
(82978 in every fetch) but not in **content**. Measured today over five fetches, three distinct
nonces and three User-Agents: raw digests `fce2d830…`, `afe5ba6f…`, `6bf2ac5e…` for the same
82978-byte body; the capture instrument's **normalized-text** digest is stable at
`cf834a65…` across three cache-busted fetches. The **PDF companion**
`https://www.first.org/standards/frameworks/psirts/FIRST_PSIRT_Maturity_Document.pdf` reproduces
round 65's recorded digest **exactly** — `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f`,
644190 bytes — matching `.ufo/waves/round-65/w1/ScoutS098/NOTES.md:91`. Receipt:
`w1/ScribeRound/receipts/F45-digest-probe.txt`. Consequence for the L1: **a F45 registry row
cannot bind the round-65 lead's raw HTML digest**; it must bind the normalized-text sha256 (or
the PDF digest) and must say which one it binds. See M67-4.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M67-1 | exemption masks incomplete input on heads other than `cat` | `.ufo/waves/round-67/controls/donothing-multihead-r67.txt` L3-L5 and L10-L12: native stage0 `-13` and gate `ok` for `cut`/`wc`/`grep` two-operand shapes whose second operand was never opened; base gate L120 `if os.path.basename(head) != "cat":` keeps every other head benign. Independently reproduced by this seat (`w1/ScribeRound/receipts/donothing-reproduce.txt`) and by RevengerMultiHead's production-gate observation (`w1/RevengerMultiHead/table.txt` TABLE F: `G-cut-2 -> ok`, `G-grep-many-2 -> ok`, `G-wc-2 -> ok`, `G-head-all-2 -> ok`, `G-tail-all-2 -> ok`). ExecMultiHeadProbes receipted the same three failures against the base gate: `PROBES probes=18 failures=3 mode=candidate`, exit 1, failures exactly P9, P10, P11 (`w1/ExecMultiHeadProbes.md`). | L1 no-work control; RevengerMultiHead; ExecMultiHeadProbes; ScribeRound | Candidate replaces the head-blind branch with a per-head counted-operand rule. Measured by this seat on the candidate (`w1/ExecMultiHeadGate/figure-audit.py`, sha256 `978c98a2c35dbd16ad66475bdd966f9ed73d17b4c642ae8210287a7345fa3a36`): `FIG P9 … derive-upstream-signal-13 stale`, `FIG P11 … derive-upstream-signal-13 stale`, `FIG P10 … stale`; single-input controls `P12`/`P13`/`P14` still `ok`; candidate selftest `cases=71 failures=0`; and the ExecMultiHeadProbes battery run against the candidate by this seat: `PROBES probes=18 failures=0 mode=candidate` exit 0 (`w1/ScribeRound/receipts/probes-vs-candidate.txt`), with P10 stale in **5 of 5** repeats under both outcome reasons (`w1/ScribeRound/receipts/candidate-P10-5-runs.txt`). **Final values pending L1 integration** — this seat measured a candidate in a seat directory, not a landed implementation, and no frozen counter exists yet. |
| M67-2 | a receipt asserts a single native status for a shape whose status is a race | `.ufo/waves/round-67/controls/donothing-multihead-r67.txt` L4 records `NATIVE P10 stages=[-13, 0]` and L11 `FIG P10 recorded=4096 big.txt derived=4096 big.txt ok`; `.ufo/waves/round-67/controls/native-statuses-r67.txt` L10 records `NATIVE P10 stages=[1, 0]` for the same shape. L1's own addendum (`controls/dispatch-addendum-r67.md`) calls P10 FLAKY. This seat measured the base gate over **12 further runs**: `FIG P10 … ok` in **10 of 12** and `FIG P10 … derive-upstream-exit-1 stale` in **2 of 12** (`w1/ScribeRound/receipts/stability-12-runs.txt`); native stage0 was `-13` in 11 of 12 and `1` in 1 of 12. | L1 dispatch addendum; ScribeRound | Do not freeze one reason for P10 and do not put P10 in the frozen repair set; the frozen repairs are cut (P9) and grep (P11), both measured `-13` on five of five L1 repeats. The candidate's selftest case `upstream-wc-multi-missing-stale-either-reason` asserts staleness under **either** reason. The two committed controls disagree and are retained; neither is rewritten. |
| M67-3 | claim wording asserts a mechanism the measurement contradicts | `w1/RevengerMultiHead.md` §6.1 and §7: `wc` reaches the later operand at every size (stderr names `missing.txt`, `strace` shows `openat(missing.txt) = -1 ENOENT`) and only then dies of `-13`; in reversed operand order `cut`/`grep`/`head-all`/`tail-all`/`cat` report the missing operand on stderr *and then* die of `-13`. The defensible statement is "a `-13` on a multi-input stage destroys the stage's own exit status and its stderr-based error is invisible to the gate", not "the operand was never read". | RevengerMultiHead | Any wording in the frozen claim, the lesson or the SCORECARD must use the status-loss formulation for `wc`; the "unread operand" formulation may be used only for `cut`/`grep`/`head`/`tail` in the operand order measured. The candidate's own docstring (measured) already says the truncation `can hide a later operand's error`, i.e. the conservative formulation. **L1 wording check pending L1 integration.** |
| M67-4 | a registry lead binds a digest that cannot be re-derived | `corpus/SOURCES.md:244` records `82978 bytes, sha256 334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e` for the F45 HTML; this seat's five fetches of the same URL yield `fce2d830…`/`afe5ba6f…`/`6bf2ac5e…` at the identical 82978-byte length (`w1/ScribeRound/receipts/F45-digest-probe.txt`); the varying bytes are the per-response CSP nonce in the script tail. The recorded digest is therefore **not reproducible** from the served HTML. | ScribeRound | Any F45 registry row must bind the **normalized-text** sha256 `cf834a65…` (stable across three cache-busted fetches and equal to ScoutF45's independent capture `w1/ScoutF45/S100.txt`) or the PDF digest `f217c446…` (which reproduces round 65 exactly), and must state which. The round-65 lead row is a **lead, not a registry row**: it may be left byte-identical and the new row may carry the re-derivable digest plus a pointer to the lead. **L1 registry decision pending L1 integration.** |
| M67-5 | the held F44 entry already names the boundary; the new ground is a different document, not an extension of S098 | `corpus/knowledge/first-psirt-services-framework.md:45` (maturity is a glossary definition, not a level ladder); S098 `grep -cE "Maturity Level\|Level [123]"` → 0; S098 L1510 and L675 are the only maturity statements; S098 L1553 links the maturity document only as a sidebar download. Measured by this seat over `corpus/knowledge/`, `SKILL.md`, `PROVINCE.md`. | ScribeRound (novelty screen); ScoutF45 (independent capture) | F45 is admitted (if at all) as its **own source id, manifest and entry**, not as an extension of S098. The F45 entry's limits section must record: the document has **no self-assessment mechanism** (measured `self-assess` count 0); the checklist is a *sample* checklist (L397), not a scored rubric; and the entry is documentation of FIRST's published levels, not evidence that any team operates at a level. **L1 admission pending L1 integration.** |
| M67-6 | a conservative refusal is not a defect report, but the cost must be named | `w1/RevengerMultiHead.md` §5.1/§6.4: with **both** operands present and fully read, `cat F G`, `cut F G`, `grep x F G`, `sort F G`, `tail -n +1 F G` all give `-13` (7/7 stable at 1 MiB and 4 MiB), so the rule marks complete worlds stale — for `sort` a pure false positive, since sort cannot mask. `tr` has no file operands at all (`tr a b F` → exit 1, `extra operand`), so an operand-count rule must not treat `tr`'s `SET1 SET2` as inputs. | RevengerMultiHead | The candidate counts operands conservatively and therefore over-refuses (option VALUES inflate the count → a safe stale). The cost is named in the candidate's docstring; the lesson, SCORECARD and report must state that the rule is a **conservative refusal, not an exact input-read test**, and that `tr` is exempted from operand counting by construction. **L1 wording check pending L1 integration.** |
| M67-7 | unknown heads keep the old benign rule, and that residual is live, not vacuous | `w1/RevengerMultiHead.md` §8: `git -C D ls-files` (20 000 index entries, 220 000 B) `\| head -n 1` → stage-0 `-13`, 5/5 — an unknown head is exempt at base. For python the benign rule is sound (a 200 000-line flood gives exit 1 `BrokenPipeError`, never `-13`). | RevengerMultiHead | Named residual: the C1 repair covers the read-only head list only; `git` and any other unknown head keep the base benign rule, so a SIGPIPE'd unknown head can still mask. It is not claimed repaired. **L1 residual wording pending L1 integration.** |
| M67-8 | production prose contradicts the repaired behaviour unless both are updated | base gate L47-L51 and L111-L115 document the *base* rule (`Other heads keep the old benign rule`); the candidate rewrites both the module docstring and the `upstream_stale` docstring, and raises `EXPECTED_CASES` 67 → 71 (`w1/ExecMultiHeadGate/figure-audit.py`). The base docstring and the base behaviour agree; only a landing that changes the executable without the prose would break this. | ScribeRound (diff of base vs candidate) | On landing, the SKILL live-gate registry row and the current-execution amendment must name the per-head counted-operand rule, the conservative over-refusal, and the unchanged unknown-head behaviour — the round-66 lesson's M66-6 shape. **L1 registry/SKILL amendment pending L1 integration.** |
| M67-9 | **the repair does not close the C1 masking class: a mid-argv `--` undercounts operands, and the masked world still reads green** | This seat imported the candidate's own `sigpipe_input_count` and measured it: `cut -f1 -d: big.txt -- -missing.txt` → **count 1, exempt True**; `grep x big.txt -- -missing.txt` → **count 1, exempt True**. Real coreutils semantics: after `--` every later token is a file operand, including a dash-named one. Native 5/5: `cut` and `grep` stage0 `-13`, stderr never names the missing operand; `strace -f -e trace=openat` under the real pipe shows `openat(big.txt)=3` and **no openat for `-missing.txt` at all**. Real gate, real ledger: **base `FIG D1 … derived=alpha ok` and candidate `FIG D1 … derived=alpha ok`** — the candidate is indistinguishable from the base on this shape. Independently found by the critic seat: `w1/CriticMultiHead/cand-shapes.txt` `S3-cut-mid-dashdash masking-dashdash rc=0 verdict=ok` and `S4-grep-mid-dashdash masking-dashdash rc=0 verdict=ok`, with the same two `ok` in `base-shapes.txt` and stage0 `[-13, 0] stable=yes` in `native-matrix-5x.txt`. | CriticMultiHead; SentinelMultiHead; ScribeRound (independent) | **Blocking for the C1 claim as frozen.** The hole needs a `--` separator (leading or mid-argv) **and** a post-`--` dash-named operand **and** a streaming head: measured affected = `cut` and `grep` only (`head`/`tail` are accidentally safe because the option VALUE inflates the count; `wc`/`sort`/`ls`/`sha256sum` never reach `-13`; `cat` is refused by the r66 cat rule). `cut` is one of the two frozen repairs (P9). The sentinel reached the same conclusion independently and states it as F1 (Low): `the change's own stated contract ("SIGPIPE is exempt only when the decoded argv names at most one input operand") is not met, so C1's closure claim must be scoped to plain multi-operand forms`. A fix must count every token after the FIRST `--` as an operand, or refuse any argv containing `--`. **This seat edits no production code; the fix, the counter re-freeze and the re-measurement are pending L1 integration.** Receipt: `w1/ScribeRound/receipts/mid-dashdash-residual.txt`. |
| M67-10 | the round-66 cat behaviour must stay byte-identical | This seat checked the AST source segment of `cat_sigpipe_exempt` in the base gate and in the candidate: **identical** (859-char source segment, `ast.get_source_segment` equality True); the candidate's only additions are the new `SIGPIPE_REQUIRED_NONFILE_ARGS` table and the new `sigpipe_input_count` function, and the cat branch still runs first and returns `not cat_sigpipe_exempt(stage_argv)`. | ScribeRound | The r66 frozen receipts must still reproduce against the candidate. This seat ran the **round-66** finite cat battery against the candidate: `CAT-MUTBAT killed=3/3 survivors=0 equivalents_held=1 invalid_rejected=1 failures=0`, `PROBES probes=8 failures=0 mode=candidate`. The sentinel seat independently replayed the r66 frozen probes against the candidate: `PROBES probes=8 failures=0`, and measured the **production ledger** unchanged: candidate `figures=35 ok=35 stale=0 exit=0`, base identical (all production derives are single-input, so the new rule changes no production figure). The r66 committed driver itself was **not** run by this seat: it refuses a `--work` outside `/fast/scratch/hyaku/kasegi-r66/`, and this seat's scratch is contractually confined to `…/kasegi-r67/ScribeRound/`. **Full r66-driver reproduction pending L1 integration** (ExecMultiHeadDriver owns the round-67 driver). |
| M67-11 | the new branch is not proven load-bearing by the mutant set's own detectors on the exit faces | SentinelMultiHead §6 F2 (Informational): `upstream-cut/wc/grep-multi-missing-stale` accept `signal-13`, `exit-1` and `exit-2`; the exit faces were already stale at base, so on a host where SIGPIPE loses the race the case passes without exercising the new rule. The mutation seat's battery (`w1/MutationMultiHead.md`) killed L4 `drop-dashdash` by `P11-dashdash-leading` and L7 `headblind-sigpipe-exempt` by `P1-cut-multi-missing` — but the three counted selftest cases themselves accept the exit faces. | SentinelMultiHead; MutationMultiHead | The asserted invariant (verdict = stale) is the right security property and the receipts now print the observed reason, so this is not a security defect. **L1 decision pending L1 integration** on whether the counted cases should assert the signal face specifically. Note that the exit faces are the same race the L1 addendum already documents (M67-2). |
| M67-12 | the F45 candidate's digest must be re-derivable, and the round-65 lead's is not | ScopeF45's screen establishes the ground is new; ScoutF45's manifest (`w1/ScoutF45/manifest.json`) records the raw-HTML digest as non-reproducible and names the PDF as the stable artifact; this seat measured the same independently (G7, M67-4). | ScopeF45; ScoutF45; ScribeRound | Any F45 registry row must bind the normalized-text sha256 `cf834a65…` or the PDF sha256 `f217c446…` and say which. **L1 registry decision pending L1 integration** (same cell as M67-4). |
| M67-13 | the F45 ladder is keyed to a **different service-catalogue version** than the one the lane holds | This seat's own capture, L356-L357: `For a complete list of supporting resources and glossary refer to the PSIRT Services Framework` / `https://www.first.org/education/FIRST_PSIRT_Services_Framework_v1.0.pdf.`; the companion PDF `CreationDate: Thu Dec 6 17:32:58 2018 -02`, 29 pages. The corpus holds the **v1.1** framework page as S098/F44. Independently reported by the scout seat: `The maturity document is older than the framework the corpus holds. … F45's level ladder is therefore keyed to the v1.0-era service catalogue.` | ScoutF45; ScribeRound (independent) | The F45 entry's limits section must state that the level ladder's service-area references are to the **v1.0** catalogue, not to S098's v1.1 page, and must not be read as a claim about the v1.1 service catalogue. **L1 entry limits pending L1 integration.** |
| M67-14 | the document's own PDF table of contents is unreliable, so no quote may be anchored to a TOC page | ScoutF45: `The PDF's table of contents is wrong in 8 of 11 checked entries` — `Level 2 heading TOC 19 → actual 10`; also Level-1 *Introduction* 3→5, *Getting Started* 3→6, *PSIRT Entrypoint* 7→8, *The Next Step* 7→8, *The Final Countdown* 9→10, Annex 1 20→21, Annex 7 27→28; only *Fixing the thing*, the Level 3 heading and *Beyond "Level 3"* are right. | ScoutF45 | Every F45 quote must be anchored to the **HTML capture's line number** (the normalized text digest `cf834a65…`), never to a PDF TOC page. This seat's own anchors (G5, Q1-Q11) are HTML capture lines and match ScoutF45's manifest anchors exactly. **L1 entry anchoring pending L1 integration.** |
| M67-15 | a verifier that cannot green the honest candidate cannot certify the claim — and the driver moved after it was measured | CriticMultiHead Finding 2 measured the driver at frozen digest `f2d11468ed39f2fa2fbafc77bc690e3ea8d049fca8c37f56f9f619096b6ae8bb`: its `parse_fig` used `re.search(r" derived=(\S+) ok$", ln)`, which cannot read a space-bearing derived value, so the driver's own P10/P13/P14 wants (`4096 big.txt`, `<hash>  big.txt`) made the **correct** gate read as `verdict=stale` → `DRIVER-RC 1` on the honest candidate. This seat ran the **current** driver `02e48a4fdac41bca64199e6a3f43e893d77702df5602e2dc5ff9ccd50898178f` against the honest candidate over a fixture commit of the wave tree: **`VERIFY measurements=12 failures=0`**, all twelve RESULTs PASS, **exit 0** (receipt: `w1/ScribeRound/receipts/driver-verification.txt`). The current `parse_fig` splits on ` derived=` and takes the whole tail before the trailing ` ok`, so the space-bearing wants parse. | CriticMultiHead (found it); ScribeRound (re-verified on current bytes) | **The false-red does not reproduce on the current driver bytes — it is a FIXED defect, not an open one.** But the L1 must pin the driver digest it freezes, because the defect was real at `f2d11468`: a frozen driver at the old digest would return `DRIVER-RC 1` on the correct gate, and that rc must not be read as a gate defect. **Final frozen driver digest, pin manifest and committed-input measurement: pending L1 integration.** |
| M67-16 | the multi-head battery does not run on the committed probes collector, and its receipt line must not be read as a silent skip | Driver RESULT line: `RESULT multihead-mutbat PASS … COLLECTOR ignored=/…/controls/probes.py reason=AttributeError`. The battery's `--collector` is optional and expects a file defining `probe_table(root)`; the committed probes collector does not define it, so `load_collector` catches the AttributeError and falls back to the battery's own built-in `probe_table(root)` — 14 named probes P1..P14 with their expected ok/stale+reason, written independently. | ScribeRound (reading the battery and the driver) | The fallback is **printed, not silent**, and the battery's `MUTBAT killed=7/7 survivors=0 equivalents=3 invalid_rejected=0 failures=0` line is the driver's PASS criterion, so the 7/7 kill result is not weakened. But the L1 must not describe the multi-head battery as "driven by the committed probes collector" — it is driven by the battery's own built-in table. **L1 wording pending L1 integration.** |
| M67-17 | a receipt states a host environment fact that was hardcoded, not measured, and it is wrong | `w1/RevengerMultiHead/table.txt` host block states `tools = cut/wc/sort/head/tail/sha256sum/tr/ls/cat 0.8.0 (uutils); grep = 'grep (pi-uu-grep) 0.2.0'`. It is a **hardcoded literal** in the seat's own `w1/RevengerMultiHead/emit_table.py` L27-L28; no probe in that seat measures tool versions. This seat measured the real PATH-resolved binaries by the same mechanism the gate uses (`shutil.which` on the bare argv[0]): **all ten are GNU coreutils 9.12 / GNU grep 3.12-modified** (`/usr/bin/cut` → `cut (GNU coreutils) 9.12`; `pacman -Qo` → `/usr/bin/cut is owned by coreutils 9.12-2`), and there is no uutils or pi-uu-grep anywhere on PATH. The reviewer seat's tool identity (`GNU coreutils 9.12, grep 3.12-modified`) is the correct one. **The revenger's NUMBERS are unaffected**: this seat re-ran its thresholds under the GNU binaries and they reproduce exactly (cat 512 KiB → rc 1 in 20/20, 513 KiB → 14×-13/6×1, 524 KiB → -13 20/20; cut 64 KiB → rc 1; grep-many → -13 10/10, grep-few → 2 10/10). | ScribeRound (measured); contradicted by the reviewer seat's independent tool identity | The revenger's **numbers stand**; only the **label** is wrong. The L1 must not copy the uutils line into any lane record: the host is GNU coreutils 9.12 + GNU grep 3.12-modified. The revenger's table is a receipt and is left byte-identical; this correction is appended (the round-66 lesson's append-only correction shape). Any threshold the L1 records must name the toolchain it was measured on and keep the race caveat. Receipt: `w1/ScribeRound/receipts/tool-identity-conflict.txt`. |
| M67-18 | input-list indirection is a surviving mask of the same class | ReviewMultiHead: `wc -l --files0-from=list0 | head -n 1` counted **zero** operands → green, and `sha256sum -c biglist | head -n 1` counted **one** operand (the list file) → green; under strace, `WIFSIGNALED(s) && WTERMSIG(s) == SIGPIPE` with **zero** `openat(... "missing.txt" ...)`, and the list's last entry `check/missing.txt` is never opened. The reviewer classifies it as `the same C1 falsification class (green on a world where a named input was never read)` and rates it `a residual/documentation gap rather than a repair defect`. This seat confirmed the shape runs: `wc -l --files0-from=list0` → rc0 1, stderr `wc: 'check/missing.txt'$'\n': No such file or directory`; `sha256sum -c biglist` → rc0 1, stderr `no properly formatted checksum lines found`. | ReviewMultiHead; ScribeRound (shape confirmed) | Pre-existing at base and **narrowed, not closed**, by the candidate. It must be named in the landing notes or the candidate docstring as a residual exemption, not left implied. **L1 residual wording pending L1 integration.** |

## Assimilation

Pending L1 integration. The read-only merge/kasegi report does not supply this gate's own-work
diagnostic. No consideration is declared implemented this round, and no knowledge, frontier or
repertoire admission is claimed by this draft. The C2 admission, if the L1 makes it, needs its
own source id, its own manifest, its own knowledge entry and its own coverage-map and Frontier
rows; this draft writes none of those.

## Open boundaries

1. **The frozen predicate and counter do not exist yet.** No `claims.json` for round 67 is
   present in the wave root. Every measured value in this draft is a seat measurement against a
   seat-directory candidate or against the unchanged base gate; none is a frozen, re-runnable
   claim. **Pending L1 integration.**
1b. **The candidate as built does not close the C1 masking class** (M67-9): a mid-argv `--` plus a
   post-`--` dash-named operand keeps the `cut` and `grep` stages exempt, and the gate reads `ok`
   on a world where that operand was never opened — measured identically at base and at the
   candidate. **A fix, a re-freeze and a re-measurement are owed before any C1 landing.**
   **Pending L1 integration.**
2. **The round-67 committed-input driver does not yet exist** in the wave tree at the time of
   this draft; `w1/ExecMultiHeadDriver/` was empty. The L1's counter, its content pins and the
   round-67 mutation battery are the L1's to freeze. **Pending L1 integration.**
3. **No coverage claim is admissible from this draft.** The F45 ground is screened as new against
   F44 and every held entry; the *admission* (registry row, manifest, knowledge entry, coverage
   map row, Frontier F45 row) is the L1's and the two F45 seats' to write. **Pending L1
   integration.**
4. **Host-specific limits of the native measurements.** The pipe capacity on this host is 65536
   bytes, but the SIGPIPE threshold is **head-specific** (≈65–70 KiB for `cut`/`grep`/`head`/`tail`,
   >512 KiB for `cat`) and is a race near each threshold, so no single repeat can freeze a
   threshold. Host tools are uutils 0.8.0 with `grep (pi-uu-grep) 0.2.0`. These numbers describe
   this host and this build only; no portable size threshold is claimed, and none is added after
   freeze. **Pending L1 integration** if the L1 records a size at all.
5. **Out of scope, unchanged from round 66 and not claimed repaired:** descendants of a stage,
   shell wrappers, PATH/configuration shadowing, filesystem races, exit-0 partial-output
   producers, and every unknown head (see M67-7). The gate is not pipefail, not a sandbox, not an
   authenticity check, and no semantic-emulator resistance is claimed.
6. **Still-unanswered operator decisions** (source restoration/province ruling, R67/R69
   counter-substance and moving-range decisions, the derive-gate security boundary, and the
   outside non-author admission/promotion) remain unanswered. This round claims no resolution.
7. **Scores are held.** depth:verifiability 4, coverage 8, depth:density 9 — no new capability,
   no retirement, no split, no stagnation waiver is asserted by this draft.
8. **A production path was written during the wave by a seat that was not the integrator.** While
   this draft was being written, `corpus/source-snapshots/round-67/` appeared as an untracked
   production directory (`S100.txt`, `S101.txt`, `manifest.json`, all timestamped 18:07 -03). This
   seat did **not** create it: this seat's own capture is under
   `w1/ScribeRound/F45-PSIRT-MATURITY.txt` and its digest `cf834a65…` is identical to the
   `S100.txt` snapshot, so this seat can neither claim nor deny authorship of the production copy.
   The manifest it carries is well-formed for this round's purpose — its `S101` record binds both
   the normalized-text sha256 `a55e315f…` (644190 raw bytes, 768 lines) **and** the
   `raw_sha256` `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f`, which this
   seat independently verified reproduces round 65's recorded PDF digest exactly, and its `S100`
   record binds the reproducible normalized-text digest `cf834a65…` rather than the round-65 lead's
   non-reproducible raw-HTML digest — which is what M67-4 and M67-12 require. **Whether the
   production write was authorized is the L1's call; this seat makes no claim about it and edits
   nothing there.** **Pending L1 integration.**

## Round-summary skeleton (to be filled by the L1 from measured values)

- **C1 (depth:verifiability, nominal 4 held).** Base `8e2a8fe8…`, gate `51f299af…`. Base
  no-work control: `NOWORK-VERDICT … green_on_masked=P9,P10,P11,P12,P13,P14` (three of those
  green figures are masked two-operand shapes). Candidate (seat copy `d5e8fcae…`): masked shapes
  `derive-upstream-signal-13 stale`; single-input controls still `ok`; candidate selftest
  `cases=71 failures=0`; round-66 cat battery `killed=3/3 … failures=0` reproduced against the
  candidate by this seat, and by the sentinel (`PROBES probes=8 failures=0`, production ledger
  `figures=35 ok=35 stale=0` identical at base and candidate). The ExecMultiHeadProbes battery
  against the candidate, run by this seat: `PROBES probes=18 failures=0 mode=candidate`, exit 0,
  with P10 stale in 5 of 5 repeats under **both** outcome reasons. The mutation seat's battery
  against the same candidate: `MUTBAT killed=7/7 survivors=0 equivalents=3 invalid_rejected=0
  failures=0`, exit 0, two identical runs. The sentinel's admission parity `MATRIX derives=96
  diffs=0` and monotone sweep `widened=0 narrowed=10 identical=42`. **BUT the C1 masking class is
  not closed**: a mid-argv `--` plus a post-`--` dash-named operand still reads `ok` at base and at
  the candidate alike, for `cut` and `grep` (M67-9). **Frozen predicate, driver digest, content
  pins, freeze/measured revisions, final committed measurement and the ledger result:
  pending L1 integration.** The **round-67 driver** exists and was run by this seat over a fixture
  commit of the wave tree: `VERIFY measurements=12 failures=0`, all twelve RESULTs PASS, exit 0,
  on the honest candidate in `--candidate` (unpinned) mode — a **trial**, not a claim
  (`w1/ScribeRound/receipts/driver-verification.txt`).
- **C2 (coverage, 8 held).** F45 = FIRST's PSIRT Maturity Document, captured independently by
  this seat and by ScoutF45 to the same normalized-text digest `cf834a65…` (478 lines). Ground:
  three named maturity levels (Basic / Intermediate / Advanced), an explicit "Beyond Level 3",
  and a per-level sample service checklist in Annex 7; measured `self-assess` count 0. Screened
  new against F44/S098 (which carries zero maturity levels) and against every held entry; the
  connector seat's independent screen over 205 files and 59 hits reached `Decision: F45's ground
  is GENUINELY NEW (UNCOVERED)` and `Coverage Verdict: IN PROVINCE`, with narrowing sentences
  against F44, F10, F13 and F43. **Registry row, manifest, knowledge entry, coverage-map row,
  Frontier F45 row, census before/after: pending L1 integration.**
- **Wave outcome.** ONE v1 wave of twelve seats. **Seat settlement, dead seats, residual calls
  and the wave verdict: pending L1 integration** (the wave had not settled when this draft was
  written; the reports of RevengerMultiHead, ExecMultiHeadGate, ExecMultiHeadProbes,
  MutationMultiHead, SentinelMultiHead and the ScopeF45 screen had landed).
- **Learning recommendations.** Expansion unchanged; quality unchanged unless the L1 mints a
  criterion for M67-2 (a receipt asserting one native status for a racy shape), M67-4/M67-12 (a
  lead digest that cannot be re-derived) or M67-9 (an operand-count rule weaker than the rule it
  sits beside); discernment improved — the round's own claim wording was falsified by a measured
  table before freeze (M67-3), a racy shape was caught before freeze by the L1's own addendum
  (M67-2), and the residual that blocks the closure claim (M67-9) was found by three independent
  seats (critic, sentinel, scribe) before any freeze. **Pending L1 integration.**
