# ScribeRound — scoped findings (kasegi round 67, wave 1)

Seat: **ScribeRound** (leaf scribe; no subagent dispatch, no `task` call, no `agent://all`).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`.
Round evidence root: `.ufo/waves/round-67`. Production gate under test:
`corpus/instruments/figure-audit.py`, sha256 `51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac`
(re-verified by this seat at the end of the wave — unchanged from base).

**Status of the round when I finished: predata only, nothing frozen, nothing landed.** No
`.ufo/waves/round-67/claims.json` existed; no freeze commit, no measured revision, no ledger
landing. **I hold no admission authority and admit nothing.** No production file was created or
modified by this seat; no commit, push, publish or deploy; no git index or jj state touched; no
pacman transaction; no tool installed or upgraded.

Report: `.ufo/waves/round-67/w1/ScribeRound.md`

## What I produced

All writes are under my seat directory and this report only:

| file | what it is |
|---|---|
| `.ufo/waves/round-67/w1/ScribeRound/lesson-draft.md` | **DRAFT** lesson in the shape of `corpus/lessons/round-66.md`: a Gate block (G1-G7, sources opened with access date and located quotes), an 18-row Mistakes table (M67-1..M67-18) grounded in wave receipts, an Assimilation paragraph, an 8-item open-boundaries list and a round-summary skeleton |
| `.ufo/waves/round-67/w1/ScribeRound/scorecard-draft-round-67.md` | **DRAFT** SCORECARD round-67 section: frozen-plan placeholders, the before/after axis table with `⟨…⟩` placeholders for L1-measured values, the residuals block, the move log and the planned-after list |
| `.ufo/waves/round-67/w1/ScribeRound/log-draft-round-67.md` | **DRAFT** LOG round-67 bullet skeleton in the file's own `- ` convention |
| `.ufo/waves/round-67/w1/ScribeRound/F45-PSIRT-MATURITY.txt` | my own independent capture of FIRST's PSIRT Maturity Document (478 lines, 59068 B, sha256 `cf834a65…`) |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/donothing-reproduce.txt` | my independent run of the L1's committed no-work control against the base gate |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/stability-12-runs.txt` | 12 further runs of that control: the P10 flake, measured |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/donothing-vs-candidate.txt` | the same control against the candidate |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/probes-vs-candidate.txt` | ExecMultiHeadProbes battery against the candidate: `PROBES probes=18 failures=0` |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/candidate-P10-5-runs.txt` | P10 stale in 5/5 repeats under **both** outcome reasons |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/mid-dashdash-residual.txt` | **the blocking residual**: the mid-argv `--` mask that survives the candidate |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/driver-verification.txt` | my independent run of the round-67 driver over a fixture commit: `VERIFY measurements=12 failures=0`, exit 0 |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/tool-identity-conflict.txt` | **host toolchain correction**: GNU coreutils 9.12 / GNU grep 3.12, not uutils |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/F45-digest-probe.txt` | the F45 digest-reproducibility measurement (raw digest rotates; normalized-text digest stable; PDF digest reproduces round 65 exactly) |
| `.ufo/waves/round-67/w1/ScribeRound/receipts/F45-raw-body.html` | the raw served body I hashed (82978 B, sha256 `fce2d830…`) |

Scratch `/fast/scratch/hyaku/kasegi-r67/ScribeRound/` is deleted before this report; the durable
receipts above are the copy.

## The finding that matters most: C1's masking class is not closed

**The candidate gate does not close the class the round opened to close.** The candidate's
`sigpipe_input_count` drops only a **leading** `--` and then treats any `-`-prefixed token as an
option; real coreutils semantics treat **every** token after `--` as a file operand. So a
post-`--` dash-named operand is dropped from the count instead of counted.

Measured by this seat, on the candidate's own function and on the real gate:

```
cut -f1 -d: big.txt -- -missing.txt   => count=1  exempt=True   (2 real operands)
grep x big.txt -- -missing.txt         => count=1  exempt=True   (2 real operands)
```

- Native 5/5: `cut`/`grep` stage 0 `-13`, stderr never names the missing operand.
- `strace -f -e trace=openat` under the real pipe: `openat(big.txt)=3` and **no openat for
  `-missing.txt` at all**.
- Real gate, real ledger: **base `FIG … derived=alpha ok` and candidate `FIG … derived=alpha ok`** —
  the candidate is *indistinguishable from the base* on this shape.

Measured scope: the hole needs a `--` separator **and** a post-`--` dash-named operand **and** a
streaming head. Affected heads measured: **`cut` and `grep` only** — and `cut` (P9) is one of the
two frozen repairs. `head`/`tail` are accidentally safe (their option VALUE inflates the count to
2), `wc`/`sort`/`ls`/`sha256sum` never reach `-13` there, and `cat` is refused by the round-66 cat
rule. **I found this independently; the critic seat found it independently (S3/S4), and the
sentinel seat found it independently (F1).** Three seats, one hole, before any freeze.

This is not a "the claim is scoped narrowly" item — the sentinel put it exactly: *the change's own
stated contract ("SIGPIPE is exempt only when the decoded argv names at most one input operand")
is not met*. I have **not** edited any production byte and have not attempted the fix; it belongs
to the candidate's owner and the L1.

## What I verified positively

- **The base masking reproduces** (my own run of the L1's committed control): `FIG P9/P11 … ok`
  on two-operand `cut`/`grep` shapes whose second operand was never opened.
- **The candidate closes the plain forms**: `PROBES probes=18 failures=0 mode=candidate`, exit 0,
  with P10 stale in 5/5 repeats under both outcome reasons; candidate selftest `cases=71
  failures=0`; the round-66 cat battery still `killed=3/3 … failures=0` against the candidate;
  `cat_sigpipe_exempt` is byte-identical between base and candidate (AST source segment).
- **The round-67 driver certifies the honest candidate on its current bytes**:
  `VERIFY measurements=12 failures=0`, all twelve RESULTs PASS, exit 0 — a **trial** over a
  fixture commit of the untracked wave tree, in unpinned `--candidate` mode, not a claim.
- **F45 is genuinely new ground.** My independent capture's normalized-text digest `cf834a65…`
  equals ScoutF45's; 11 located quotes with HTML-capture line anchors; `self-assess` count 0 (no
  self-assessment mechanism); S098 carries zero `Maturity Level|Level [123]` matches; the
  connector seat's independent 205-file screen reached `GENUINELY NEW (UNCOVERED)`.

## Other findings the L1 needs

1. **The P10 shape is racy and the committed controls disagree** — `donothing-multihead-r67.txt`
   L4 records `-13`, `native-statuses-r67.txt` L10 records `1`. My 12 further runs: base green in
   **10**, stale in **2**. The L1's own addendum already caught this and forbade freezing P10.
2. **The round's claim wording was falsified by a measured table before freeze** — `wc` *does*
   reach its later operand (strace `openat(missing.txt) = -1 ENOENT`) and then dies of `-13`; in
   reversed operand order `cut`/`grep`/`head`/`tail`/`cat` likewise report the missing operand and
   *then* die of `-13`. The defensible statement is "a `-13` destroys the stage's own exit status
   and hides its stderr-based error", not "the operand was never read".
3. **The round-65 lead's F45 digest is not re-derivable** — the page carries a per-response CSP
   nonce: five fetches of the identical 82978-byte body gave three different raw digests
   (`fce2d830…`, `afe5ba6f…`, `6bf2ac5e…`). The normalized-text digest `cf834a65…` is stable; the
   PDF digest `f217c446…` reproduces round 65 exactly. **Any F45 row must bind a re-derivable
   digest and say which.**
4. **The F45 ladder is keyed to the v1.0 service catalogue**, not to S098's v1.1 page (Annex 1
   L356-L357 → `FIRST_PSIRT_Services_Framework_v1.0.pdf`; PDF `CreationDate` 2018-12-06). The
   document's own PDF TOC is wrong in 8 of 11 checked entries, so every quote must be anchored to
   the HTML capture line, never a TOC page.
5. **Host toolchain correction.** The host's ten read-only tools are **GNU coreutils 9.12 / GNU
   grep 3.12-modified** (measured via the same `shutil.which` the gate uses; `pacman -Qo` →
   `coreutils 9.12-2`, `grep 3.12-2`; no uutils on PATH). `w1/RevengerMultiHead/table.txt`
   states `0.8.0 (uutils)` / `pi-uu-grep 0.2.0` — a **hardcoded literal** in that seat's
   `emit_table.py` L27-L28, not a measurement. The revenger's *numbers* reproduce exactly under
   GNU (cat 512 KiB → rc 1 20/20; 513 KiB → 14×-13/6×1; 524 KiB → -13 20/20; cut 64 KiB → rc 1),
   so its threshold findings stand and only its label is wrong. **The L1 must not copy the uutils
   line into any lane record.**
6. **The critic's driver false-red is fixed, not open** — its `parse_fig` regex
   `derived=(\S+) ok$` could not read a space-bearing want, so the *correct* gate read as stale at
   the critic's frozen driver digest `f2d11468`. The current driver parses those wants and greens
   the honest candidate. **The L1 must pin the driver digest it freezes.**
7. **The multi-head battery runs on its own built-in probe table**, not the committed probes
   collector (`COLLECTOR ignored=… reason=AttributeError` — the collector simply lacks the
   optional `probe_table` API). The fallback is printed, not silent, and the 7/7 kill result is not
   weakened; but the L1 must not describe the battery as "driven by the committed probes
   collector".
8. **A production path was written during the wave by a seat that was not the integrator.**
   `corpus/source-snapshots/round-67/` (`S100.txt`, `S101.txt`, `manifest.json`) appeared as an
   untracked production directory at 18:07 -03. **This seat did not create it** — my own capture
   lives under `w1/ScribeRound/`, and its digest `cf834a65…` is identical to the `S100.txt`
   snapshot, so I can neither claim nor deny authorship of the production copy. Its manifest is
   well-formed for this round's purpose (it binds the reproducible normalized-text digest and the
   round-65-reproducible PDF `raw_sha256`). **Whether that write was authorized is the L1's call;
   I edit nothing there.**

## Out of scope, and not claimed

- No sandbox, semantic-emulator resistance, general shell correctness, pipefail or authenticity
  claim is made anywhere in my drafts.
- The gate is not pipefail and not a sandbox; descendants, wrappers, PATH/configuration shadowing,
  filesystem races and exit-0 partial-output producers remain outside the repair.
- Unknown heads (`git`, `python`) keep the base benign rule; the residual is **live** — `git
  ls-files` (20 000 entries) `| head -n 1` gives stage-0 `-13` 5/5 — and is **not** claimed
  repaired. Input-list indirection (`wc --files0-from`, `sha256sum -c`) is a further same-class
  mask, narrowed not closed.
- The rule is a **conservative refusal, not an exact input-read test**: with both operands present
  and fully read, `cat F G`, `cut F G`, `grep x F G`, `sort F G` and `tail -n +1 F G` all die of
  `-13`, so complete worlds are marked stale (for `sort` a pure false positive).
- No threshold is claimed as portable; the SIGPIPE boundary is head-specific and racy on this host.
- No tool was installed or upgraded; no pacman transaction was performed.

## What the L1 still owes

The lesson, SCORECARD and LOG drafts are complete as drafts. Every value I could not source from
a wave receipt is marked **`pending L1 integration`** rather than invented (20 such markers in the
lesson). The L1 must fill: the frozen predicate and counter, the driver digest and content pins,
the freeze/measured revisions, the final committed-input measurement, the census before/after, the
registry/manifest/knowledge/coverage-map/Frontier rows for F45, the wave settlement, and the
decision on the mid-`--` residual — which, on the evidence here, **blocks landing the candidate as
it stands**.
