# Round 67 — multi-head SIGPIPE input-count gate (C1) and FIRST PSIRT maturity F45 (C2)

Two claims, one v1 wave of 12 seats. C1 lowest depth:verifiability 4 held nominal under R58; C2
coverage 8 held. Base `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`; frozen claims
`.ufo/waves/round-67/claims.json` (freeze `b30820609b033003550f0a99624337f8d50ebef3`); measured
implementation **`c40f0bc8ae95627b60b6f6e893ea00d7b1fd7146`**, production gate sha256
`8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247`.

## Gate

**S100 — FIRST PSIRT Maturity Document, HTML page.** https://www.first.org/standards/frameworks/psirts/psirt_maturity_document
opened 2026-11-04 (HTTP 200, 82978 fetched bytes, normalized snapshot 59068 bytes / 478 lines,
sha256 `cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f`, content L216-L464).
Located quote (≤25 words, L224): "in this document is intended to describe a profile of a product
security team" — admitted for the level ladder and its own definition of maturity; refused for any
certification, score, SLA or service-catalogue reading. Two seats captured the page independently
and their snapshot digests agree.

**S101 — the same document's PDF companion.** https://www.first.org/standards/frameworks/psirts/FIRST_PSIRT_Maturity_Document.pdf
opened 2026-11-04 (HTTP 200, raw 644190 bytes, sha256 `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f`,
byte-stable across two fetches; text layer 58889 bytes / 768 lines, sha256 `a55e315f…`). Located
quote (≤25 words, L8): "believes are best practices. These descriptions are for informational
purposes only" — admitted because the HTML rendering does not carry the non-normativity notice.

**Refusals recorded in the registry.** The round-65 lead's raw-HTML digest `334aeb01…` is not
reproducible (per-response CSP nonce: six fetches, six raw digests, identical 82978-byte length,
one normalized digest) and is carried into no row (R100). The per-level service-area listings are
PNG artwork and are refused as text claims; the PDF's table of contents is wrong in 8 of 11
checked entries and is refused as an anchor source.

**Own-work diagnostics (not domain sources).** The gate under test at base (`51f299af…`), the
no-work control `controls/donothing-multihead-r67.txt`, the measured base/face matrices and the
critic's differential receipt are own-work evidence for a local instrument, not new domain ground
and not a frontier admission.

Assimilation: none. `merge/kasegi/` was not used this round; the latest `considerthese/` proposal
remains domain-task-open and no consideration is declared implemented. No still-unimplemented
proposal is claimed.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M67-1 | payload expectation contradicts production | `controls/base-matrix-r67.txt`: P1/P2 read `derive-upstream-signal-13` at base (round-66's cat repair is already in production) and P8's native stage0 is 0 so no candidate can derive a signal; the payload said `P1/P2 base rc0` and `P8 candidate signal-13` | R93; L1 base matrix measured before dispatch | Payload preserved; correction committed as `controls/dispatch-addendum-r67.md` and delivered to ExecMultiHeadGate, ExecMultiHeadProbes and ExecMultiHeadDriver before they froze their batteries |
| M67-2 | flaky native face frozen as one expectation | `controls/native-statuses-r67.txt` (P10 = 1) versus `controls/face-matrix-r67.txt` (P10 = −13 ten of ten); the probes seat measured 3/5 green where the candidate requires stale | R94; L1 repeat probes | P10/P11/P19/P20 became verdict-level with an any-of reason set; the driver loops to the −13 face and records a `FACE` line per attempt |
| M67-3 | gate rule under-counts a dash-named operand after a mid-argv `--` | `w1/CriticMultiHead.md` S3/S4 `masking-dashdash rc=0 verdict=ok` with native −13 five of five and `-missing.txt` never opened; independently reproduced in `controls/critic-s3s4-confirm-r67.txt` | R95; critic seat, confirmed by L1 | Candidate re-cut (argv split at the first `--` anywhere); two counted selftest cases and probes P19/P20 added before the freeze |
| M67-4 | counter scored a bound instrument's diagnostic line as a failure | first `--final`: `collector-ignored-FAIL COLLECTOR fixtures=ok`, while the receipt also prints `probes=collector:d56a1437…(probe_table) count=33 … collector=19` | R96; the measurement itself | Erratum 1 narrowed the assertion to a literal ` ignored=` line plus a required `probes=collector:` binding; other `COLLECTOR` lines are recorded as findings |
| M67-5 | two writers on one pinned control | a duplicated `WC_REASONS` definition after the L1 and the mutation seat both patched the battery | R97; the driver seat noticed the file changing under it | Seat told to stop writing; L1 removed the duplicate, froze the bytes and pinned them |
| M67-6 | claims digest transcribed from an earlier reading | `claims.json` names the battery `e6d54540…`; the commit and pins carry `88e0c3e6…` | R98; L1 pin refresh | Corrected in `claims-erratum-1.md` E2, not rewritten in the frozen file |
| M67-7 | battery equivalence controls flipped with the wc face | `controls/erratum2-mutbat-flaky-receipt.txt`: `equivalents=1 invalid_rejected=2 failures=2`, `MUTANT E1 … invalid by=not-equivalent` | R94/R97; second `--final` | Erratum 2: the `DIFFERENTIAL` rows resolve to `("stale", WC_REASONS)`; three standalone runs then agreed on `equivalents=3 invalid_rejected=0 failures=0` |
| M67-8 | raw response digest pinned as a source anchor | six fetches of the FIRST maturity page give six raw digests at an identical 82978 bytes; the r65 lead's `334aeb01…` reproduces under no normalization | R100; scout seat, confirmed by scribe seat's independent capture | Lead retired as S100/S101 with the correction in `corpus/SOURCES.md`; the row pins the normalized snapshot digest |
| M67-9 | final measurement not written to a receipt file | the first `--final` ran without a redirect; only its RESULT/VERIFY lines survived and the failing measurement's receipt had to be copied out of the scratch tree afterwards | R99; L1 | Every later `--final` writes `controls/final-verification-r67.txt` in the same command |
| M67-10 | post-commit edit of a pinned control | the worktree battery differed from the committed bytes after the pinning commit | R97; L1 worktree/pin digest comparison | Worktree reverted to the committed bytes; the newer bytes are not measured and not carried |

## Round shape and settlement

One v1 wave, 12 seats: ExecMultiHeadGate, ExecMultiHeadProbes, ExecMultiHeadDriver (executor ×3),
ReviewMultiHead (reviewer), CriticMultiHead (critic), MutationMultiHead (mutation-tester),
SentinelMultiHead (sentinel), RevengerMultiHead (revenger), ScoutF45 (scout), ScopeF45 (connector),
ScribeF45 and ScribeRound (scribe ×2). L1 holds the planner seat (the validator rejects a planner
role). No residual call, no dead seat, no replacement. Attack seats: reviewer, critic,
mutation-tester, sentinel, revenger = 5 of 12 (42 %). Seat iterations after the first settle
(the gate re-cut, the probes' 20-row revision, the driver's defect fixes and the bounded unfreeze)
are part of the same wave and are recorded above; they are not extra seats.

`w1-results.json` holds the orchestrator's per-seat record; several seats' `final` fields are null
under the dispatcher's kernel-restart limitation, so the seats' own reports in `w1/` are the
evidence used here, not those nulls.

## Final measurement and adjudication

Predicate (frozen before data): **VERIFY measurements=12 failures=0 and process exit0 on the exact
committed-input counter.** Final run at `c40f0bc8ae95627b60b6f6e893ea00d7b1fd7146`,
receipt `.ufo/waves/round-67/controls/final-verification-r67.txt`:

```
RESULT probes-measured PASS mode=candidate probes=20 rc=0 … FACES measured attempts=P9:sig20/other0 P10:sig12/other1 P11:sig20/other0 P19:sig20/other0 P20:sig20/other0 faces-clean
RESULT shape-identity PASS shapes=20
RESULT selftest PASS cases=73 failures=0
RESULT mutbat-existing PASS killed=5/5
RESULT multihead-mutbat PASS killed=7/7 equivalents=3 invalid_rejected=0 failures=0
RESULT real-ledger PASS FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
RESULT red-wrong-want PASS  RESULT identity-guards PASS gate=8147350c… base=51f299af…
VERIFY measurements=12 failures=0 revision=c40f0bc8ae95 mode=final
```

C1 verdict: **verified** on the frozen predicate, delta 0 (nominal R58 — the axis's
citation-resolution metric is not read by this gate). C2 verdict: **verified** — frontier 44 → 45,
registry 99 → 101, entries 47 → 48, capture records 79 → 81, knowledge 82 → 83, census exit 0.

Adjudication of seat findings:
- **CriticMultiHead's mid-argv `--` finding is accepted and was fixed before the freeze**; the
  critic's other survivors (exit-0 partial-output producers, wrapper/descendant stages,
  `git`/`python` heads, option-value false stales) are named residuals, not repairs. Its
  driver-defect findings (parse_fig, base-kind expectation, collector-ignored) became the driver's
  three ordered fixes and erratum 1.
- **SentinelMultiHead** verdict FINDINGS: F1 (pre-existing masking not closed — the `git`/`python`
  heads) is named as a residual; F2 (test strength) is accepted; no widening, no new admitted head
  or flag, no write path — the admission parity matrix reports 96 derives and 0 diffs.
- **ReviewMultiHead** accepts the production-path repair with the same-class residual and
  documentation gaps; its option-value refusal table matches the candidate's conservative rule.
- **MutationMultiHead**'s seven-limb battery kills 7/7 with three equivalents; its battery needed
  the face-tolerant DIFFERENTIAL patch (erratum 2), and its post-freeze edits are M67-5/M67-10.
- **RevengerMultiHead** measured the native premise (head/tail/sort/wc/sha256sum never reach −13 on
  the two-operand shapes; cut/grep do) and its uutils-versus-GNU binary note became the PATH
  residual.
- **ScoutF45 / ScopeF45 / ScribeF45** ground C2; the scout found the non-reproducible raw digest
  (M67-8) and the PDF's wrong TOC; the connector's independent sweep found no held maturity ground.

## Open boundaries

Source restoration and province re-point (L0 kasegi r15), counter-substance and moving-range
decisions (r57 R67/R69), the derive-gate security boundary (r59/r60) and the four authorized
fresh-start rulings remain unanswered and untouched. This round claims no resolution of them.
`git`/`python` head masking, wrappers, descendants, exit-0 partial-output producers,
PATH/configuration, filesystem races and semantic emulators beyond the finite forgeries stay
outside the guarantee. Scores 4/8/9 held; no capability row, retirement, split or nudge waiver.

Learning: expansion **improved** (F45 admitted with an 18-row claim table on ground the lane did
not hold); quality **unchanged** (no knowledge entry superseded or re-verified; the instrument
repair is a gate correction); discernment **improved** (the wave's attack seats found the mid-argv
hole, the flaky face and three counter defects before the freeze, and this round's own errata were
filed rather than hidden). Outside non-author admission and promotion remain owed; SHONEN stays
author-asserted.
