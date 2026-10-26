# MutC2Entry — round 38 (C2 mutation probe: F21 entry provenance)

Seat: MutC2Entry (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Item: mutate the F21 entry provenance five ways and run harness / recheck-audit / source-recheck per
mutant, recording exit codes and failing lines. Scratch: `/fast/scratch/hyaku/kasegi-r38/MutC2Entry/`
(removed before yield). No tool install, no network fetch, no lane write outside this receipt.

Lane state at work time: HEAD `700153593eb586c70a6499c8ca225ee4d673bc9b`; the round-38 landing was in
progress in the working tree (uncommitted `M PROVINCE.md`, `M corpus/README.md`, …). The landed bytes
used here were verified identical to the wave1 deliverables before mirroring (`cmp` silent):

- `corpus/knowledge/csaf-vex-product-status-and-justifications.md` == `wave1/ScribeEntryF21.entry.md`
- `corpus/source-snapshots/round-38/S055.txt` == `wave1/ExecC2Capture.S055.txt`
  (sha256 `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`, 5146 lines, 272441 bytes)
- `corpus/source-snapshots/round-38/manifest.json` == `wave1/ExecC2Capture.manifest.json`
  (sha256 `95b3f46d9c502573f299ed565325a0db27009c2a5eb50205c1ca27b3556f9a9f`)
- landed entry sha256 `0343ef4544ebd675754c498829fa99bbde4f1391d4260db5e494efe8a6dc5b0a`

No deliverable file: this seat lands findings only, nothing for the L1 to copy.

## 1. Mirror design (two mirrors, one delta)

- **A (form mirror, recheck-audit)** — `cp -a <lane>/corpus A/corpus`, entry bytes as landed
  (`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`). Audit run as
  `recheck-audit.py --root A --cdroot <lane>` (the flag exists exactly for scratch copies: *“set it
  when --root is a scratch copy of the corpus”*).
- **B (execution mirror, harness + source-recheck)** — same copy, with the entry's `cd` target
  rewritten `…/kasegi-shokunin` → `…/kasegi-r38/MutC2Entry/B` (single path substitution, all other
  bytes identical). Hermeticity is load-bearing: `frontier-recheck-count.py` *executes* the recheck
  line, and with the committed `cd <lane>` prefix it would run against the lane's manifest, making
  mirror mutations invisible. `diff -rq A/corpus B/corpus` reports only the entry file.
- Working dir for every run: the mirror root (`--root A/B`, `cwd=B` for source-recheck); `TMPDIR=$S`.

## 2. Baselines (mutant-free, both mirrors)

```
$ python3 A/corpus/instruments/recheck-audit.py --root $S/A --cdroot <lane>            # rc=0
csaf-vex-product-status-and-justifications.md   frozen=111 strict=111111 lane=0 foreign=0 executes PASS
lines=50 total=50 pass=50 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=50 missing=0 unexpected=0 exit=0

$ python3 B/corpus/instruments/frontier-recheck-count.py --root $S/B                   # rc=0
PASS  F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055  exit=0
entries=24 pass=24 exit=0

$ cd $S/B && python3 corpus/instruments/source-recheck.py \
    --manifest corpus/source-snapshots/round-38/manifest.json --source S055            # rc=0
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=2135-ok
S055:Q2 OK occurrences=1 anchor=2844-ok
S055:Q3 OK normalized=markup-whitespace occurrences=1 anchor=2151-ok
S055:Q4 OK occurrences=1 anchor=1767-ok
```

Green on all three, so every mutant delta is attributable. (F21's harness citation limb holds via the
entry's FC-2 line `grep -oF <word> S055.txt | wc -l`, the only `S055` mention outside the
declaration/recheck lines.)

## 3. Mutants and verdicts

Driver: scratch `driver.py` — apply mutation to A+B, run the trio, restore pristine bytes, assert
sha256 after every restore. Six probes, ~5 s each.

| # | mutation | recheck-audit (A) | harness (B) | source-recheck (B) | verdict |
|---|---|---|---|---|---|
| a | entry `source: S055` → `source: S054` | rc 0, F21 PASS (blind) | **rc 1**: `FAIL F21 … ids=S054 exit=- problems=header-sources-not-rechecked,selection-not-declared-by-entry`; `entries=24 pass=23 exit=1` | rc 0 (blind) | **killed** (harness) |
| b | `verified-at: 2026-10-26` → `verified-at: 2026-99-99` | rc 0, F21 PASS | rc 0: `PASS F21 … exit=0`; `entries=24 pass=24 exit=0` | rc 0, Q1–Q4 OK | **SURVIVED** all three |
| c | `recheck:` line → `recheck: The pinned capture is re-verified by hand whenever this entry is updated.` | **rc 1**: `frozen=110 strict=110100 lane=127 foreign=127 gated FAIL`; `instrument_fail=1 own_fail=1 paths_fail=1`; `lines=50 total=50 pass=49 … exit=1` | **rc 1**: `FAIL F21 … problems=not-a-recheck-invocation,no-source-selection,no-manifest`; `entries=24 pass=23 exit=1` | rc 0 (blind) | **killed** (audit + harness) |
| d | entry file deleted (README row + expected-list line kept) | **rc 1**: `missing=corpus/knowledge/csaf-vex-product-status-and-justifications.md`; `expected=50 missing=1 unexpected=0 exit=1`; `lines=49 total=49 pass=49` | **rc 1**: `FAIL F21 … ids=- problems=missing-entry`; `entries=24 pass=23 exit=1` | rc 0 (blind) | **killed** (audit + harness) |
| e | manifest Q1 quote, one word: `…is to state that…` → `…is to show that…` | rc 0, F21 PASS (blind) | **rc 1**: `FAIL F21 … ids=S055 exit=1 problems=recheck-exit-1`; `entries=24 pass=23 exit=1` | **rc 1**: `S055:Q1 MISMATCH reason=quote-not-found` (Q2–Q4 still OK) | **killed** (source-recheck + harness) |
| e′ | entry Claim-1 blockquote, one word: `> "The main purpose of the VEX format…` → `> "The main goal of the VEX format…` (line 24; em-dash/`L2135` untouched) | rc 0, F21 PASS | rc 0: `PASS F21 … exit=0`; `entries=24 pass=24 exit=0` | rc 0, Q1–Q4 OK | **SURVIVED** all three |

Exact failing lines are quoted above verbatim from the instrument stdout (full outputs in scratch
`out/mutants2.json`, mirrored into §3 verbatim).

## 4. Findings

1. **(b) `verified-at:` is machine-unchecked — survived.** No instrument parses it: `grep -rn
   "verified-at" corpus/instruments/` matches only the selftest fixture
   `limb-fixtures/fr/fr-duplicate-entry/corpus/knowledge/dup-entry.md:4`, never instrument code.
   The harness reads `source:`/evidence/`recheck:` lines only; recheck-audit reads `recheck:` lines
   only; source-recheck validates the manifest (its provenance rule checks the manifest's
   `fetched_utc`, not the entry header) and the capture. Empirically all three stayed rc 0 with
   `2026-99-99` in the header. Coverage finding, not a contract change: the field is enforced only
   by human review (QUALITY), and `2026-99-99` — an impossible date — passes the whole shelf.
2. **(e′) entry-prose quotes are unpinned — survived.** The pin chain is entry → manifest Q-quotes →
   capture; only the manifest leg is machine-checked (mutant e kills through it). A one-word change
   to a blockquote in the entry body is invisible to all three instruments. Control:
   `anchorcheck.py` on the entry prints `0 in-range cite instances, 0 bad; 0 distinct anchors` —
   the entry cites as `(L2135)`, not as backticked `path:NN` cites, so anchorcheck has nothing to
   grab. Entry-quote fidelity therefore rests entirely on the manifest pins plus the seat receipt's
   FC-1 table (human artifact). Any one-word drift between entry prose and capture between rounds
   would go undetected.
3. **(a) killed, but only by the harness's declared-set limbs.** `S054` is a real registry id
   (F20/SSVC), so the meaningful failure is the binding, not the string: `ids=S054` with
   `header-sources-not-rechecked` + `selection-not-declared-by-entry`. This matches ExecC2Harness
   r5's finding that a *self-consistent* S054 binding would fall through to `manifest-missing-ids`
   — the round-38 manifest listing only S055 is what closes that route.
4. **(c) precision on the parse limb.** Prose alone does *not* fail `parse`: `bash -n` accepts
   “The pinned capture is re-verified …” as a simple command (`frozen=110` — parse=1, cwd=1 because
   both cwds exit 127 with equal digests). The frozen limb that fails is `paths` (no `corpus/…`
   token); the strict set adds `instrument_fail` and `own_fail`, and the line classifies `gated`
   (runs, fails closed, 127=127). The audit docstring's “not prose with a trailing parenthetical”
   example is the parse-limb case; plain prose without parentheses sails through parse.
5. **(d) rejection is expected-list-driven.** With the entry deleted but its `knowledge-expected.txt`
   line kept, the audit's remaining 49 entries all pass (`lines=49 total=49 pass=49`) and the only
   failure is `missing=…` — the sync control ExecC2Audit proved from the other side (`unexpected=1`).
   The harness adds the independent `missing-entry` record via the README row.

## 5. Restoration evidence

- After every mutant, the driver rewrote the four overlay files from pristine copies and asserted
  `sha256 == pristine` (entry A, entry B, manifest, capture) before the next probe.
- Post-loop: `cmp` A-entry vs landed lane entry → identical; B-entry asserted to carry the hermetic
  `cd $S/B` prefix and pristine text (`verified-at: 2026-10-26`, `is to state that and why`).
- Post-restore trio re-run, all green: audit rc 0 `expected=50 missing=0 unexpected=0`; harness rc 0
  `entries=24 pass=24 exit=0`; source-recheck rc 0 with Q1–Q4 OK.
- Scratch dir `/fast/scratch/hyaku/kasegi-r38/MutC2Entry/` removed before this receipt was
  finalized (G6 quiescence).

## 6. Method note (first run discarded)

The first driver run had a defect: `restore()` wrote the lane-cd variant of the entry into mirror B,
so the harness executed the recheck against the *lane's* (unmutated) manifest — file-scoped mutants
(a, c, d) were unaffected but (e)'s harness PASS was contaminated. Detected by reasoning about the
(e) result, fixed by pinning a separate pristine B-entry (`pristine/entry-B.md`), and **all six
probes re-run**; §3 reports the clean second run (`out/mutants2.json`) only.

## 7. Tooling / scope

No tools installed or upgraded; no network; no pacman; no mutating git (only read-only `git -C
<lane> log/status`); no writes outside scratch and this receipt. The lane working tree changed
during the session because the L1 was landing wave1 concurrently; my mirrors snapshot that tree and
all landed bytes were `cmp`-verified against the wave1 deliverables first (§0 hashes).
