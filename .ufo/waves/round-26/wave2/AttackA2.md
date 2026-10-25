# AttackA2 — C1 counter (b) gameability probe (round 26, wave 2)

Seat: `L1Kasegi26.AttackA2` (mutation tester / falsifier). Attacked claim: **C1 (b)** —
`grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` returns `1`, and the
receipt's selftest line is backed by a true 15-case run. Run 2026-10-25 (UTC), lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Scratch-only: no production file modified.

## 1. Verdict
- The **counter itself** returns `1` on the real receipt (claim verified, `count=1`).
- But the counter is **gameable**: a forged scratch receipt whose `selftest cases=` line is
  injected by hand — no instrument run, no selftest — still returns `1`. The counter is a
  presence check on a text prefix; it does not verify the run occurred, the case count, or
  the failure claim. A surviving coverage/finding, not a contract change.
- The **backing** of the real receipt's line is real: `e1-selftest-live.txt` records a live
  15-case run at the landed instrument digest (all `ok`, `selftest_exit=0`), and the index's
  `## regeneration history` note ties the 15 to the landed digest post-ExecAuditFix. So the
  real line is true — but the counter alone cannot establish it.

## 2. Counter verification on the real receipt
Command (exact claim command):
```
grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt
```
Output: `1` (match is line 4: `selftest cases=15 failures=0 exit=0`).
Receipt hash (before/after identical): `e2ab7b93f82af4f6752480909029c703f1b26badbe3b2c4b1280948c65e104dc`.

## 3. Mutation probe — forged line, no run
Method: copy real receipt to scratch; strip the genuine selftest line; hand-inject the same
claim text; never invoke the instrument. Scratch artifacts in `/tmp/a2-scratch/`.

| Scratch file | Mutation | `grep -cE 'selftest cases='` | sha256 |
|---|---|---|---|
| `receipt-pristine.txt` | none (control) | 1 | `e2ab7b93…` |
| `receipt-forged.txt` | selftest line replaced by hand-injected `selftest cases=15 failures=0 exit=0` — **no run** | **1** | `7c7adbed…` |
| `receipt-absurd.txt` | hand-injected `selftest cases=999 failures=999 exit=9` | **1** (content-blind) | `f91da631…` |
| `receipt-noselftest.txt` | selftest line removed (negative control) | 0 | `973625ef…` |

Findings:
- A misleading `selftest cases=15 failures=0 exit=0` line produced with **no run** yields
  counter `1` — identical to the genuine receipt. The counter cannot distinguish.
- The counter is content-blind: `cases=999 failures=999 exit=9` also counts `1`; any line
  beginning `selftest cases=` matches. It does not validate `cases=15`, `failures=0`, or
  `exit=0`.
- Thus C1b's counter enforces only "some selftest-cases line exists", not "a true 15-case
  run happened".

## 4. Backing verification — is the real line backed by a true 15-case run? Yes.
1. **Live evidence `c1-controls/e1-selftest-live.txt`** (generated 2026-10-25T12:37:35Z):
   - Header: `## --selftest (15 cases)`.
   - 13 per-entry case rows (good/prose/cwd/ghost/degenerate/elsewhere/ownonly/selftesty/
     sourced/basetest/basestate/parseonly/instonly — lines 7–19), all `ok`.
   - 2 expected-list cases (`expect-missing`, `expect-unexpected` — lines 27, 35), both `ok`.
   - Auxiliary `selftest completeness lines=13 total=15 complete=False ok` (completeness is a
     sanity row, not a case — matches instrument comment "completeness … not counted as a case").
   - `selftest_exit=0` (line 36). ⇒ 13 + 2 = **15 cases, all ok, exit 0**.
   - `instrument_sha256=3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` —
     matches the landed digest.
2. **Instrument source** `corpus/instruments/recheck-audit.py` computes `total_cases =
   len(cases) + 2` (line 302) with comment: "13 per-entry fixtures + 2 tree-level expected-list
   fixtures (completeness is an auxiliary sanity line above, not counted as a case)" → 15.
   The e1 live output implements exactly this.
3. **Index regeneration note** (`c1-receipt-index.txt` `## regeneration history`): "regenerated
   at the landed instrument digest 3fc0d751… after ExecAuditFix landed (selftest cases 14 →
   15; expect-list active; expected list regenerated to 39 entries)". Ties the 15 to the landed
   bytes after the fix.
4. **Digest chain consistent**: receipt `instrument_sha256=3fc0d751…` =
   `c1-instrument-digest.txt` `instrument=3fc0d751…` = e1 `instrument_sha256=3fc0d751…` =
   `sha256sum corpus/instruments/recheck-audit.py` = `3fc0d751…`. The receipt line sits at the
   instrument's own digest, as the claim requires.
5. **Caveat (honest)**: the landed instrument does **not** emit a `selftest cases=…` stdout
   line (current source has no such print; only the old round-25 fixture version did, at
   `c1-controls/fixtures/base/…/recheck-audit.py:221`, printing `cases=14`).
   The receipt line is therefore committed summary text — consistent with e1's live output and
   the source-computed 15 — not a verbatim stdout capture. The defense is the e1 evidence +
   regeneration note + digest match, all of which verify.

## 5. Control / restoration evidence
- Real receipt hash before and after all probes: `e2ab7b93…` → `e2ab7b93…` (unchanged; no
  production edit). Scratch artifacts live only in `/tmp/a2-scratch/` (hashes above).
- No tooling installed (used preinstalled `grep`, `sed`, `sha256sum`, `python3` read-only);
  no pacman/uv/npx activity; no VCS writes.

## 6. Outcome
Mutant injected = forged `selftest cases=15 failures=0 exit=0` line without any run.
Detector run = the C1b counter. Result: detector returns `1` on the mutant — the counter
survives the forgery, i.e. it is insufficient as a truth gate. The real receipt's line is
backed (e1 + regeneration note + digest match), so the after-state is factually true; the
finding is that the **counter is gameable** (presence-only, content-blind).
Recommendation for the owners (not applied here): the counter should at least verify the
receipt's digest line against `c1-instrument-digest.txt` and cross-check the `cases=15`
figure against `e1-selftest-live.txt`; a line alone proves nothing.
