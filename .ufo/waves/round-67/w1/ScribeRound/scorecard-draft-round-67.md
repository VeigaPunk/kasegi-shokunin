# SCORECARD round-67 — DRAFT skeleton (seat ScribeRound)

**DRAFT. Not landed.** No production file was created or modified by this seat. The L1 is the
sole production integrator; every `⟨…⟩` placeholder is a value only the L1 can fill from a
measured, frozen run. A placeholder is **not** a measured value and must never be reported as
one. Shapes are copied from the landed round-66 section
(`SCORECARD.md`, "Round66 measured result") so the L1 can paste and fill.

---

## Round 67 — multi-head SIGPIPE input-completeness (C1, depth:verifiability, nominal 4 held) and F45, the FIRST PSIRT maturity levels (C2, coverage, 8 held)

Frozen claims: ⟨`.ufo/waves/round-67/claims.json` freeze ⟨hash⟩, base
`8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`, driver ⟨digest⟩⟩; measured implementation
⟨**⟨hash⟩** (candidate sha256 ⟨digest⟩, cmp-pinned in the driver's `input_sha256`)⟩.
Counting command: ⟨`python3 -B .ufo/waves/round-67/w1/ExecMultiHeadDriver/verify.py --revision REV
--controls-revision ⟨hash⟩ --work /fast/scratch/hyaku/kasegi-r67/L1/MEASUREMENT [--final]`⟩.
Before uses the base revision and omits `--final`. **Final measurement still owed.**

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | Exact base `8e2a8fe8` gate `51f299af…`: base no-work control prints `NOWORK-VERDICT gate=corpus/instruments/figure-audit.py green_on_masked=P9,P10,P11,P12,P13,P14` — three of those (`cut`/`wc`/`grep` two-operand shapes) read `ok` although the second operand was never opened (`controls/donothing-multihead-r67.txt` L3-L5, L10-L12; `controls/native-statuses-r67.txt`); selftest 67/0 | ⟨Committed final: VERIFY ⟨N⟩ measurements=⟨M⟩ failures=⟨0⟩ exit⟨0⟩ at ⟨measured rev⟩; masked shapes `cut`/`grep`/⟨wc⟩ read `derive-upstream-signal-13 stale` under the frozen predicate; single-input controls `cut`/`wc`/`sha256sum` stay `ok`; selftest 71/0; round-66 cat battery `killed=3/3 survivors=0 equivalents_held=1 invalid_rejected=1`; multi-head mutant battery `killed=⟨K⟩/⟨K⟩ survivors=⟨0⟩`; real ledger ⟨N⟩/⟨N⟩; wrong-want red/right-want green⟩ | **4 → 4, delta 0, nominal per R58** (source-availability/citation-resolution metric not moved; the non-moving metric is named). ⟨Counting command above, REV=⟨measured rev⟩; receipt `.ufo/waves/round-67/controls/⟨file⟩`⟩ |
| coverage | ⟨`FRONTIER-CENSUS rows=44 admitted=44 closed=44 problem-rows=0 registry=99`; `entries=47 pass=47`; capture `records=79 bound=79 unbound=0`; expected ⟨N⟩ lines / ⟨N⟩ paths; knowledge 82; F45 absent (lead only, `corpus/SOURCES.md:244`); census exit 0⟩ (base counters measured at `controls/c2-base-counters-r67.txt`) | ⟨`rows=⟨N⟩ admitted=⟨N⟩ closed=⟨N⟩ problem-rows=⟨0⟩ registry=⟨100⟩`; `FRONTIER-PASS F45 ids=⟨S100⟩`; `entries=⟨N⟩ pass=⟨N⟩`; `records=⟨N⟩ bound=⟨N⟩ unbound=⟨0⟩`; expected ⟨N⟩ lines / ⟨N⟩ paths; knowledge ⟨N⟩; census exit 0⟩ | **8 → 8, delta 0** (if the L1 admits F45) ⟨`python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-67/manifest.json --source ⟨S100⟩` (⟨N⟩ Q-OK)⟩ |
| depth:density | 9 | 9 held | Not targeted or re-measured. SKILL changes are one registry row's factual cells (selftest 67→71, the per-head counted-operand SIGPIPE rule) plus a current-execution amendment; no density credit asserted. |

**BLOCKING RESIDUAL — the C1 claim must not be frozen or landed as-is.** The candidate's
`sigpipe_input_count` drops only a **leading** `--` and then treats any `-`-prefixed token as an
option, so a **mid-argv** `--` followed by a dash-named operand undercounts the operands:
measured on the candidate's own function, `cut -f1 -d: big.txt -- -missing.txt` → count 1,
exempt True; `grep x big.txt -- -missing.txt` → count 1, exempt True. Real coreutils semantics
treat every token after `--` as a file operand. Native 5/5: `cut`/`grep` stage0 `-13`, stderr
never names the missing operand, and `strace -f -e trace=openat` under the real pipe shows
`openat(big.txt)=3` with **no openat for `-missing.txt`**. The real gate on a real ledger reads
`FIG D1 recorded=alpha derived=alpha ok` at **base and at the candidate alike** — the candidate
is indistinguishable from the base on this shape. Measured affected heads: **`cut` and `grep`
only** (`head`/`tail` are accidentally safe because the option VALUE inflates the count to 2;
`wc`/`sort`/`ls`/`sha256sum` never reach `-13` on this shape; `cat` is refused by the r66 cat
rule). `cut` is one of the two frozen repairs (P9). Independently found by the critic seat
(`w1/CriticMultiHead/cand-shapes.txt` S3/S4 `masking-dashdash rc=0 verdict=ok`). Receipt:
`w1/ScribeRound/receipts/mid-dashdash-residual.txt`. **A fix must count every token after the
FIRST `--` as an operand, or refuse any argv containing `--`; the counter must then be
re-frozen and re-measured. Pending L1 integration — this seat edits no production code.**

**Two further residuals of the same class, measured by the reviewer seat and confirmed here.**
(i) **Input-list indirection:** `wc -l --files0-from=list0 | head -n 1` counts **zero** operands and
`sha256sum -c biglist | head -n 1` counts **one** (the list file); both read green while the list's
entries are never opened. Pre-existing at base, **narrowed not closed**; must be named in the
landing notes. (ii) **Unknown heads** keep the base benign rule, and the residual is live —
`git ls-files` (20 000 entries) `| head -n 1` gives stage-0 `-13` 5/5, so a SIGPIPE'd unknown head
can still mask; for python the benign rule is sound (a 200 000-line flood exits 1
`BrokenPipeError`, never `-13`).

**Host toolchain — the correct identity is GNU, and the revenger's label is wrong.** The host's
ten read-only tools are **GNU coreutils 9.12 / GNU grep 3.12-modified** (PATH-resolved by the same
`shutil.which` the gate uses; `pacman -Qo` → `coreutils 9.12-2`, `grep 3.12-2`; no uutils on PATH).
`w1/RevengerMultiHead/table.txt` instead states `0.8.0 (uutils)` / `pi-uu-grep 0.2.0`, which is a
**hardcoded literal** in that seat's `emit_table.py` L27-L28, not a measurement. The revenger's
**numbers reproduce exactly** under the GNU binaries (cat 512 KiB → rc 1 20/20, 513 KiB → 14×-13/
6×1, 524 KiB → -13 20/20; cut 64 KiB → rc 1; grep-many → -13 10/10), so its threshold findings
stand and only its label is wrong. **The L1 must not copy the uutils line into any lane record.**
Receipt: `w1/ScribeRound/receipts/tool-identity-conflict.txt`.

**Residuals named, not claimed:** the rule is a **conservative refusal, not an exact input-read
test** — with both operands present and fully read, `cat F G`, `cut F G`, `grep x F G`, `sort F G`
and `tail -n +1 F G` all die of `-13` on this host, so complete worlds are marked stale (for
`sort` a pure false positive; `sort` cannot mask). `tr` takes no file operands, so its `SET1 SET2`
must never be counted as inputs. **Unknown heads keep the base benign rule** — measured live:
`git ls-files` (20 000 entries) `| head -n 1` gives stage-0 `-13` 5/5, so a SIGPIPE'd unknown head
can still mask; for python the benign rule is sound (a 200 000-line flood exits 1
`BrokenPipeError`, never `-13`). Out of scope and not claimed repaired: descendants of a stage,
shell wrappers, PATH/configuration shadowing, filesystem races, exit-0 partial-output producers.
The gate is not pipefail, not a sandbox, not an authenticity check. The threshold at which a
head SIGPIPEs is **head-specific and racy** on this host (≈65–70 KiB for `cut`/`grep`/`head`/`tail`,
>512 KiB for `cat`, pipe capacity 65536 B) — no portable size threshold is claimed.

**Caveat carried into the frozen text:** `wc` does **not** die of SIGPIPE *before* reaching its
later operand — it reaches it (stderr names the missing file; `strace` shows `openat(missing.txt) =
-1 ENOENT`) and only then dies of `-13` on a later write of its own summary lines; its status is
a race (`-13` or `1`). The defensible formulation is "a `-13` on a multi-input stage destroys the
stage's own exit status and its stderr-based error is invisible to the gate", not "the operand was
never read". `wc`'s reason is therefore **not** frozen to one value; the frozen repair set is
`cut` (P9) and `grep` (P11).

**F45 ground, if admitted (pending L1 integration):** FIRST's *PSIRT Maturity Document* — three
named maturity levels (1 Basic, 2 Intermediate, 3 Advanced), an explicit "Beyond Level 3", and a
per-level **sample** service checklist in Annex 7. Measured `self-assess` count 0: the document
carries **no self-assessment mechanism**, and the checklist is a sample, not a scored rubric. The
entry would be FIRST's published levels, not evidence that any team operates at a level. Screened
new against F44/S098, whose capture carries **zero** `Maturity Level|Level [123]` matches (the
only maturity statements are the S098 glossary entry at L1510 and one measurement remark at L675),
and against every held entry (one held file mentions maturity at all, and it is the F44 boundary
sentence itself). **Any F45 registry row must bind a re-derivable digest** — the normalized-text
sha256 `cf834a65…` (stable across three cache-busted fetches; equal to the independent ScoutF45
capture) or the PDF sha256 `f217c446…` (which reproduces round 65 exactly). The round-65 lead
row's **raw** HTML digest `334aeb01…` is **not** re-derivable — the page carries a per-response
CSP nonce, so five fetches of the identical 82978-byte body yield three different raw digests.
**Two further F45 boundaries the entry must carry:** (i) the ladder is keyed to the **v1.0**
service catalogue (Annex 1 L356-L357 points at
`FIRST_PSIRT_Services_Framework_v1.0.pdf`; PDF `CreationDate` 2018-12-06), **not** to S098's
v1.1 framework page, so a F45 statement about the services a level expects is a statement about
the v1.0 catalogue; and (ii) the document's own PDF table of contents is wrong in 8 of 11 checked
entries (Level 2 heading: TOC 19, actual 10), so **every quote must be anchored to the HTML
capture's line number**, never to a PDF TOC page.

**Capabilities:** no new row. The existing `derive-gate-chain-refusal` row is extended in place —
the gate now also refuses a multi-operand read-only head that was SIGPIPE'd. **Demonstration:**
⟨`python3 -B .ufo/waves/round-67/w1/ExecMultiHeadDriver/verify.py --revision ⟨hash⟩ --final` →
⟨N⟩/⟨0⟩⟩.

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability 4,
worked nominally this round; the nudge is not active. No retirement or split.

### Round-67 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 67 | depth:verifiability | SIGPIPE'd non-cat read-only heads exempt at base (`cut`/`wc`/`grep` two-operand shapes read `ok` although the second operand was never opened); selftest 67 | multi-operand read-only heads refused on the per-head counted-operand rule; `cut`/`grep` masked shapes read `derive-upstream-signal-13 stale`; single-input controls `ok`; selftest 71 | `.ufo/waves/round-67/controls/donothing-multihead-r67.txt`; `controls/native-statuses-r67.txt`; `controls/dispatch-addendum-r67.md`; `corpus/instruments/figure-audit.py` |
| 67 | coverage | frontier ⟨44⟩ / registry 99 / entries 47 / capture 79 / knowledge 82; F45 a **lead only**, never admitted | frontier ⟨N⟩ / registry ⟨100⟩ / entries ⟨N⟩ / capture ⟨N⟩ / knowledge ⟨N⟩; F45/⟨S100⟩ admitted with ⟨N⟩ anchored quotes | `.ufo/waves/round-67/controls/c2-base-counters-r67.txt` → ⟨final⟩; `corpus/knowledge/⟨file⟩`; `corpus/source-snapshots/round-67/` |
| 67 | calibration | round-66 routed defects carried in; two r67 defects found **before** freeze (a racy shape asserted with one native status; a lead digest that cannot be re-derived) and one claim wording falsified by a measured table | ⟨both r67 defects addressed in the frozen text; M67-2 and M67-4 rows in the lesson; R-rows in QUALITY if the L1 mints them⟩ | `corpus/lessons/round-67.md` (draft: `w1/ScribeRound/lesson-draft.md`); `corpus/QUALITY.md` |

### Planned after round 67 (not frozen)

1. **depth:verifiability (4, lowest):** the next gate claim must select a distinct observed
   residual with a failing no-work control. Candidates visible in this round's measurements:
   the **unknown-head** residual (`git` SIGPIPEs 5/5 and stays exempt), the **exit-0 partial-output**
   class, or the **descendant/wrapper** class. Do not re-claim the multi-head input-count rule.
2. **coverage (8):** F45's maturity ladder is new ground; the Fuzzilli primary docs and the OpenSSF
   aggregate-score/API portion remain unopened leads requiring their own source/novelty/claim-table
   gates. A maturity ladder is a **level taxonomy, not a capability measurement**; any future claim
   about a team's actual operating level would need evidence this lane does not hold.
3. **Digest hygiene for mutable HTML sources:** a source whose served bytes carry a per-response
   nonce cannot be bound by a raw-body digest. Future captures of such pages should record the
   normalized-text sha256 (or a PDF digest) in the manifest, and the row should say which artifact
   it binds. **Pending L1 integration** — whether this becomes a QUALITY row is the L1's call.
