# LOG round-67 — DRAFT bullet skeleton (seat ScribeRound)

**DRAFT. Not landed.** No production file was created or modified by this seat; the L1 is the
sole production integrator. Convention copied from the landed `LOG.md` round-66 section: each
bullet is one `- ` line under a `## Round 67 (<date>) — <title>` heading, bullets carry the
durable path of the receipt they rest on, and every claim a bullet states must be backed by a
committed receipt. **`⟨…⟩` placeholders are values only the L1 can fill from a measured run;
a placeholder is not a measurement.** Bullets whose whole content is already measured in this
wave are given in full; bullets that depend on the freeze, the driver, the census or the wave
settlement are left as skeletons.

---

## Round 67 (2026-11-04) — multi-head SIGPIPE input-completeness, predata construction

- C1 only, lowest depth:verifiability 4 nominal held under R58; coverage 8 held; base
  `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`, gate sha256
  `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac`. The chosen residual is the
  round-66 completion of M65-7: the base gate's SIGPIPE exemption is **head-blind** for every
  non-`cat` read-only head (`corpus/instruments/figure-audit.py` L120
  `if os.path.basename(head) != "cat":`), so a streaming head dies of SIGPIPE before reaching a
  later named operand and the gate reads `ok` on a world where a named input was never read.
  Durable command/output/exit: `.ufo/waves/round-67/controls/donothing-multihead-r67.txt`
  (L3-L5 native `-13`; L10-L12 gate `ok`; L19
  `NOWORK-VERDICT gate=corpus/instruments/figure-audit.py green_on_masked=P9,P10,P11,P12,P13,P14`).
- The measured masking is **not** limited to `cut`/`wc`/`grep`: `head -n <large>` and `tail -n +1`
  also read `ok` on a world whose second operand was never opened
  (`.ufo/waves/round-67/w1/RevengerMultiHead/table.txt` TABLE F). Base masking therefore covers
  five read-only heads, all inside the gate's own allow-list.
- **A shape's native status is a race, and the first committed receipt froze it.** `wc -l big.txt
  missing.txt | head -n 1` (P10) is measured `-13` in
  `.ufo/waves/round-67/controls/native-statuses-r67.txt` L10 and `-13` in
  `controls/donothing-multihead-r67.txt` L4, while the L1's own repeat probe found `1`; the L1
  correction `.ufo/waves/round-67/controls/dispatch-addendum-r67.md` calls P10 FLAKY, forbids
  freezing one reason for it, and fixes the frozen repair set to `cut` (P9) and `grep` (P11).
  ScribeRound measured the base gate over 12 further runs: `FIG P10 … ok` in 10 and
  `FIG P10 … derive-upstream-exit-1 stale` in 2 (`w1/ScribeRound/receipts/stability-12-runs.txt`).
  Both committed controls are retained, neither is rewritten.
- The round's own claim wording was **falsified before freeze** by a measured table: `wc` does not
  die of SIGPIPE *before* reaching its later operand — it reaches it (stderr names the missing file;
  `strace` shows `openat(missing.txt) = -1 ENOENT`) and only then dies of `-13` on a later write of
  its own summary lines, and in reversed operand order `cut`/`grep`/`head`/`tail`/`cat` likewise
  report the missing operand and *then* die of `-13`
  (`.ufo/waves/round-67/w1/RevengerMultiHead.md` §6.1, §7). The defensible statement is that a
  `-13` on a multi-input stage destroys the stage's own exit status and hides its stderr-based
  error — not that the operand was never read.
- ONE twelve-seat predata build/falsify v1 handoff, `.ufo/waves/round-67/w1-spec.json` and
  `w1-dispatch.json`, plus the L1's amended spec `w1-spec-amended-r67.json` and the 17:53 -03
  correction `controls/dispatch-addendum-r67.md`. L1 planner; three executors, reviewer, critic,
  mutation-tester, sentinel, revenger, scout, connector and two scribes. Production remains
  unchanged while controls and the candidate are built; this is not a freeze or an admission.
- Candidate construction: `w1/ExecMultiHeadGate/figure-audit.py` replaces the head-blind branch
  with a per-head counted-operand rule (cat/cut/head/tail/sort/wc/sha256sum/ls/tr = 0 required
  non-file args, grep = 1 for its pattern; a leading `--` is dropped, an option token is not an
  operand, option VALUES inflate the count and so over-refuse safely). The round-66
  `cat_sigpipe_exempt` is **byte-identical** in the candidate (AST source segment equality, checked
  by ScribeRound) and the cat branch still runs first, so the round-66 frozen behaviour is
  unchanged. Candidate selftest `cases=71 failures=0` (base 67/0); the **round-66** finite cat
  battery still passes against the candidate: `CAT-MUTBAT killed=3/3 survivors=0 equivalents_held=1
  invalid_rejected=1 failures=0`. The candidate is a construction artifact, not yet a frozen claim
  or a production improvement.
- The rule is a **conservative refusal, not an exact input-read test**: with both operands present
  and fully read, `cat F G`, `cut F G`, `grep x F G`, `sort F G` and `tail -n +1 F G` all die of
  `-13` on this host (7/7 stable), so complete worlds are marked stale — for `sort` a pure false
  positive, since `sort` cannot mask. `tr` takes no file operands (`tr a b F` → exit 1 `extra
  operand`), so `SET1 SET2` must never be counted as inputs. The SIGPIPE threshold is
  head-specific and racy (≈65–70 KiB for `cut`/`grep`/`head`/`tail`, >512 KiB for `cat`; pipe
  capacity 65536 B); no portable size threshold is claimed or added after freeze.
- **Unknown heads keep the base benign rule, and that residual is live.** `git ls-files`
  (20 000 index entries, 220 000 B) `| head -n 1` gives stage-0 `-13` 5/5, so a SIGPIPE'd unknown
  head is still exempt at base; for python the benign rule is sound (a 200 000-line flood exits 1
  `BrokenPipeError`, never `-13`). The C1 repair does not cover unknown heads and does not claim
  to.
- **The candidate does not close the C1 masking class: a mid-argv `--` undercounts operands.**
  `sigpipe_input_count` drops only a **leading** `--` and then treats any `-`-prefixed token as an
  option, so `cut -f1 -d: big.txt -- -missing.txt` and `grep x big.txt -- -missing.txt` count as
  **one** operand (exempt True), while real coreutils semantics treat every token after `--` as a
  file operand. Native 5/5: stage0 `-13`, stderr never names the missing operand, and
  `strace -f -e trace=openat` under the real pipe shows `openat(big.txt)=3` with **no openat for
  `-missing.txt`**. The real gate on a real ledger reads `FIG D1 recorded=alpha derived=alpha ok`
  at **base and at the candidate alike**. Measured affected heads: `cut` and `grep` only
  (`head`/`tail` accidentally safe because the option VALUE inflates the count; `wc`/`sort`/`ls`/
  `sha256sum` never reach `-13`; `cat` is refused by the r66 cat rule); `cut` is one of the two
  frozen repairs (P9). Found independently by the critic seat
  (`w1/CriticMultiHead/cand-shapes.txt` S3/S4 `masking-dashdash rc=0 verdict=ok`). **The C1 claim
  must not be frozen or landed until the counter counts every token after the FIRST `--` as an
  operand (or refuses any argv containing `--`) and is re-measured.** Receipt:
  `w1/ScribeRound/receipts/mid-dashdash-residual.txt`. ScribeRound edits no production code.
- **Host toolchain correction.** The host's read-only tools are **GNU coreutils 9.12 / GNU grep
  3.12-modified** (PATH-resolved by the same `shutil.which` the gate uses; `pacman -Qo` →
  `coreutils 9.12-2`, `grep 3.12-2`; no uutils on PATH). `w1/RevengerMultiHead/table.txt` states
  `0.8.0 (uutils)` / `pi-uu-grep 0.2.0` — a **hardcoded literal** in that seat's `emit_table.py`
  L27-L28, not a measurement. The revenger's **numbers reproduce exactly** under the GNU binaries
  (cat 512 KiB → rc 1 20/20, 513 KiB → 14×-13/6×1, 524 KiB → -13 20/20; cut 64 KiB → rc 1;
  grep-many → -13 10/10), so its threshold findings stand and only its label is wrong. **The uutils
  line is not copied into any lane record**; the revenger's table is left byte-identical and this
  correction is appended. Receipt: `w1/ScribeRound/receipts/tool-identity-conflict.txt`.
- **Input-list indirection is a surviving mask of the same class.** `wc -l --files0-from=list0 |
  head -n 1` counts zero operands and `sha256sum -c biglist | head -n 1` counts one (the list
  file); both read green while the list's entries are never opened. Pre-existing at base, narrowed
  not closed; named in the landing notes rather than left implied.
- **The round-67 driver certifies the honest candidate on its current bytes.** Trial run by
  ScribeRound over a fixture commit of the wave tree (`git init` fixture, toplevel asserted before
  the first commit; the wave tree is untracked in the lane, so the driver cannot read its controls
  from a lane revision): `VERIFY measurements=12 failures=0`, all twelve RESULTs PASS, exit 0, on
  the honest candidate in `--candidate` (unpinned) mode. This is a **trial, not a claim**. It also
  shows the critic seat's driver `parse_fig` false-red (`derived=(\S+) ok$`, which cannot read a
  space-bearing want) was **fixed** in the current driver bytes — the L1 must pin the driver digest
  it freezes, because the defect was real at the critic's frozen digest `f2d11468`. Receipt:
  `w1/ScribeRound/receipts/driver-verification.txt`.
- C2 (coverage): F45 is FIRST's *PSIRT Maturity Document*, a round-65 **lead** that was opened only
  for boundary screening and never admitted (`corpus/SOURCES.md:244`). It was captured this round
  independently by ScoutF45 and by ScribeRound to the **same** normalized-text digest
  `cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f` (478 lines, 59068 bytes),
  HTTP 200, `Last-Modified: Mon, 26 Jan 2026 14:43:46 GMT`. Its ground is new against F44: S098
  carries **zero** `Maturity Level|Level [123]` matches (only the glossary entry at L1510 and one
  measurement remark at L675), and exactly one held file mentions maturity at all — the F44
  boundary sentence itself (`corpus/knowledge/first-psirt-services-framework.md:45`). The document's
  own structure is three named levels (1 Basic, 2 Intermediate, 3 Advanced), an explicit "Beyond
  Level 3", and a per-level **sample** service checklist in Annex 7; measured `self-assess` count
  is **0**, so it carries no self-assessment mechanism and the checklist is not a scored rubric.
  Two further F45 boundaries the entry must carry: the ladder is keyed to the **v1.0** service
  catalogue (Annex 1 L356-L357 points at `FIRST_PSIRT_Services_Framework_v1.0.pdf`; the companion
  PDF's `CreationDate` is 2018-12-06), **not** to S098's v1.1 framework page; and the document's
  own PDF table of contents is wrong in 8 of 11 checked entries (Level 2 heading: TOC 19, actual
  10), so **every quote must be anchored to the HTML capture's line number**, never to a PDF TOC
  page. The connector seat's independent screen over 205 files and 59 hits reached `Decision:
  F45's ground is GENUINELY NEW (UNCOVERED)` and `Coverage Verdict: IN PROVINCE`, with narrowing
  sentences against F44 (horizontal catalogue vs vertical ladder), F10, F13 and F43.
- **A lead row's raw digest is not always re-derivable.** The round-65 lead records the F45 HTML
  as `82978 bytes, sha256 334aeb01…`; five fetches of the same URL today yield three different raw
  digests (`fce2d830…`, `afe5ba6f…`, `6bf2ac5e…`) at the **identical** 82978-byte length, because
  the page carries a per-response CSP nonce in its script tail. The capture instrument's
  normalized-text digest is stable, and the PDF companion reproduces round 65's digest exactly
  (`f217c446…`, 644190 bytes). Any F45 registry row must bind a re-derivable digest and say which.
  Receipt: `w1/ScribeRound/receipts/F45-digest-probe.txt`.
- Frozen claims: ⟨`.ufo/waves/round-67/claims.json`, freeze ⟨hash⟩, predicate ⟨verbatim⟩⟩.
  Nominal 4 held under R58; the counter, its content pins, the round-67 driver and the multi-head
  mutant battery are the L1's to freeze. ⟨The round-66 driver itself was not run by ScribeRound:
  it refuses a `--work` outside `/fast/scratch/hyaku/kasegi-r66/`, and this seat's scratch is
  contractually confined to `…/kasegi-r67/ScribeRound/`; ExecMultiHeadDriver owns the round-67
  driver.⟩
- Implementation after freeze ⟨hash⟩: integrate the candidate byte-exactly into
  `corpus/instruments/figure-audit.py`; the per-head counted-operand SIGPIPE rule replaces the
  head-blind branch, the cat rule stays byte-identical, four public-path selftests are added
  67→71, and the module docstring plus the SKILL live-gate registry row and current-execution
  amendment name the conservative over-refusal and the unchanged unknown-head behaviour.
- Final committed measurement at ⟨hash⟩, after WAVE-DONE: ⟨counting command⟩ prints
  `VERIFY measurements=⟨N⟩ failures=⟨0⟩ exit⟨0⟩` and all ⟨N⟩ RESULTs pass
  (`.ufo/waves/round-67/controls/⟨file⟩`, raw ⟨children⟩/). Same prefreeze no-work base
  ⟨N⟩/⟨M⟩ exit⟨1⟩; no postfreeze counter amendment. Production gate ⟨digest⟩ matches the freeze;
  ledger ⟨N⟩/⟨N⟩ and the required positives are retained.
- Wave settled ⟨N⟩:⟨M⟩ evidence reports, ⟨D⟩ dead seats ⟨names and the observed terminal error,
  not an inferred one⟩; no replacement or residual call. ⟨The wave had not settled when this
  draft was written.⟩
- End frontier census ⟨0⟩ before/after, ⟨six inherited W04 warnings⟩; ⟨S100⟩ only, registry
  99→100, tiers ⟨A⟩/⟨B⟩/⟨C⟩ held, mined ⟨N⟩/rejected ⟨N⟩ held, zero old row changes
  (`controls/source-counts.txt`). Actual gap ⟨N⟩ rechecks/⟨N⟩ gated/⟨0⟩ broken
  (`controls/score-gap-after.txt`). Coverage 8 / density 9 held.
- Required fleet-root misroot sweep exits 0 (`controls/fleet-misroot-sweep.txt`); no owned misroot.
  No tool installs or routing/host changes, pacman untouched. Only this lane round open.
  Final documentation/receipt commit follows the measured implementation without changing the
  gate/counter/pins; the report cites both the measured revision and the pushed final lane hash.
