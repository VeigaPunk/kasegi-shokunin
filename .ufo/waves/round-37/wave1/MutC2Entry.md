# MutC2Entry — F20 entry provenance-field mutation test (round 37, C2 / coverage)

Seat `MutC2Entry-2` (leaf mutation-tester; no subagent dispatched). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(read-only to this seat except this receipt). Base `b56a41680cefd391868c1c370dc063c69d827e7d`, claims freeze
`224df74db2a46d627ae1475a72ca48796bbd177c`, lane HEAD observed `b362068195d5489aa94b31e6ec8f880c367e0ba0`
(claims-erratum-1). Claim served: C2 coverage — the planned F20 (SSVC) knowledge entry's provenance fields.

**Item.** Mutate the planned F20 entry's provenance fields and show the instruments reject them:
(a) `source:` → S053; (b) `verified-at:` malformed; (c) `recheck:` prose-only/non-executable; (d) entry missing.
Run the relevant instrument (harness/audit/source-recheck) on a scratch mirror per mutation and record the failure.

**Bottom line.** Three of the four mutants are killed: (a) by the harness (rule A, both directions),
(c) by the harness AND the recheck-audit (parse limb), (d) by the harness (fail-closed `missing-entry`) AND the
audit (expected-list set equality, `missing=1`). Mutant (b) — a malformed `verified-at:` header — **survives every
committed C2 instrument** (harness, recheck-audit, source-recheck, capture-binding-check all stay green), for two
independent malformation classes. That survivor is a coverage finding, recorded as measured: no committed
instrument reads the `verified-at:` field; its Q1 enforcement lives with the reviewing seat, not in an instrument
limb. Every mutation was applied to a scratch mirror only; the lane tree's `corpus/` was never touched; every
mutated file was restored byte-exact (hash-verified) and the mirror re-verified green after each restore.

## 1. Mirror: the planned post-landing state

Built at `/fast/scratch/hyaku/kasegi-r37/MutC2Entry/mirror` (removed before this receipt was finalized; all hashes
below were measured while it existed):

- Base: `git archive HEAD -- corpus | tar -x` at lane HEAD `b3620681` (corpus/ is byte-identical to base
  `b56a4168`: `git diff --stat b56a416 224df74 -- corpus/` is empty and `b3620681` adds only `.ufo/` files).
- Planned artifacts, each extracted from the owning seat's receipt and **hash-verified before use**:

| artifact | source receipt | bytes | sha256 | verified |
|---|---|---|---|---|
| F20 README block (§3, appended at EOF) | `wave1/ScribeFrontierAmendments.md` | 2947 | `2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b` | exact match to the receipt's stated block hash |
| S054 registry row (after `\| S053 \|`, line 60) | `wave1/ScribeRowS054.md` §1 | 866 | `83020b30ca32fd49c2a1cd85864792d01004a594b59ad2f13fb83e1e6f734f03` | exact match |
| knowledge entry (84 lines) | `wave1/ScribeEntryF20.md` §2 fenced block | 12594 | `5b0ae4e04d8608129e84448f91fcfee7c2df335fe8014375c23e912c16b0fba8` | header L3 `source: S054`, L4 `verified-at: 2026-10-26`, L5 `ground: F20`, L6 executable `recheck:` |
| capture `S054.txt` (518 lines) | re-fetched live with the lane's `capture-source.py` at the erratum-1 URL | 32623 | `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21` | equals the pin in `ExecC2Capture`/`ExecC2QuoteOnce`/`ScribeEntryF20`/`RevEntryF20` |
| `round-37/manifest.json` | `wave1/ExecC2Capture.md` §4 (the byte-exact landing instruction) | 3989 | `fabc3163dbd31d33bff6e0bccf8b86b94e081b06b3ab1f00538dd9c0a57df642` | exact match; parses as JSON |
| `knowledge-expected.txt` sync (+1 line, C-sorted position 40) | `wave1/ExecExpectedListSync.md` §2 | 2514 | `92aa812447f516b88f07146591e1ee05421860cf677b283162c2d3f4ada474ce` | exact match to that seat's synced-list hash |

- Mirror claim-target cross-check (frozen C2 counting commands): frontier rows `20`; SOURCES `S###` rows `54`;
  files citing `^source: S054 ` → `1`; knowledge files `49`; expected-list entry lines `49` (`LC_ALL=C sort -c`
  clean).

**Documented mirror adaptation (not a mutation).** Every committed `recheck:` line carries an absolute
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix (47 of 48 pre-existing entries; `root-loss-2026-10-12.md`
has none). In the mirror those prefixes were rewritten to the mirror root, **on `recheck:` lines only**
(47 files, one line each; `considerthese-proposals-ledger.md` and `epss-exploit-prediction-scoring.md` carry the
lane path in prose/code blocks too — those lines were left untouched). Without this, the harness executes the F20
line against the live lane, where `corpus/source-snapshots/round-37/` does not exist yet, and the pristine baseline
fails `recheck-exit-2` — exactly `ExecC2Harness` variant M — making every mutant inconclusive. The adaptation is
identical across pristine/mutated/restored states, so the only byte delta per mutation is the assigned mutation
itself. Proof: un-adapting the mirror's F20 entry (mirror path → lane path) reproduces the planned entry
byte-for-byte (`diff` clean against the `ScribeEntryF20` §2 extraction). Resulting subject hashes:

- planned entry (unadapted): `5b0ae4e04d8608129e84448f91fcfee7c2df335fe8014375c23e912c16b0fba8` (12594 B)
- pristine mirror subject (adapted): `7b2214bf2108c01d8ad723f74d355db9e2f6cbc24b55e5592c1e2b04d87f2b0c` (12597 B, +3 = the longer cd target)

Instrument identity: the mirror ran the lane's own committed instruments, byte-identical to the lane working tree —
`frontier-recheck-count.py` `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249`,
`recheck-audit.py` `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09`,
`source-recheck.py` `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`,
`capture-binding-check.py` `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` (each `SAME` lane vs
mirror; the first, second and fourth match the hashes `ExecC2Harness`, `ExecExpectedListSync` and
`ExecManifestChecks` recorded independently).

## 2. Pristine baseline (before any mutation) — green

Run from a neutral cwd with `--root <mirror>` (audit additionally `--cdroot <mirror>`; `--json` receipts written
outside the mirror):

```text
harness   : PASS F20 knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054 exit=0
            entries=23 pass=23 exit=0                                   exit=0
audit     : strict pass=49/49 cdroot_fail=0 instrument_fail=0 own_fail=0
            lines=49 total=49 pass=49 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
            expect=present expected=49 missing=0 unexpected=0 exit=0     exit=0
source-
recheck   : S054:sha256 OK / Q1 anchor=259-ok / Q2 anchor=277-ok / Q3 anchor=473-ok / Q4 anchor=68-ok
                                                                          exit=0
capture-
binding   : records=44 bound=44 unbound=0  (context instrument)          exit=0
```

Selftests (instrument sanity, `HYAKU_SCRATCH` bound to the seat scratch): harness `selftest cases=6 failures=0`
exit 0; audit selftest exit 0 (18 `ok` fixture lines); source-recheck `selftest cases=10 failures=0` exit 0.

The baseline is exactly the frozen C2 after-state (`entries=23 pass=23 exit=0`, `expected=49 unexpected=0`), so a
mutation verdict below is conclusive, not a baseline artifact.

## 3. Mutation table

Each row: mutate → run harness + audit + source-recheck (capture-binding as context) → record → restore →
re-verify. Subject file hash before every mutation: `7b2214bf…f2b0c`; restored hash identical every time.

| id | mutant (exact change) | sha256 after | harness | recheck-audit | source-recheck | capture-binding (ctx) | verdict |
|---|---|---|---|---|---|---|---|
| (a) | L3 `source: S054 ` → `source: S053 ` (header id only; URL/capture text unchanged) | `72a356242a40bef073aac6ff9ddc1bb53e89b771043347ca06dc89c0a08bafae` | **FAIL** `problems=header-sources-not-rechecked,selection-not-declared-by-entry`, `entries=23 pass=22 exit=1` | exit 0 (`strict 49/49`, `expected=49 missing=0 unexpected=0`) — survives | exit 0 — survives | exit 0 | **KILLED** by harness |
| (b) | L4 `verified-at: 2026-10-26` → `verified-at: 2026-13-45` (not a real calendar instant; L83's prose mention untouched) | `e7fa357656162f213150fc426389dde61152921385b3f2ead9236a32ebffc30f` | exit 0, `entries=23 pass=23` — survives | exit 0, `expected=49 missing=0 unexpected=0` — survives | exit 0 — survives | exit 0 | **SURVIVED** (all instruments) |
| (b2) | L4 → `verified-at: pending` (placeholder class; the class `capture-binding-check` rejects in manifests) | `d80d2a08a7ec5bc0b108eb6e51643c401b750507a1bbb42c97a0442895bf0fe2` | exit 0, `entries=23 pass=23` — survives | exit 0 — survives | exit 0 — survives | exit 0 | **SURVIVED** (all instruments) |
| (c) | L6 executable recheck → `recheck: Re-run the SSVC overview capture check each round and update the anchors if the page moved (see QUALITY Q10).` | `bb0f85eced0086c6319fca71ac78f6ef94d9506ecbf7d2a21672372b3b684ff5` | **FAIL** `problems=not-a-recheck-invocation,no-source-selection,no-manifest`, `entries=23 pass=22 exit=1` | **FAIL** `parse_fail=1 paths_fail=1`, `strict pass=48/49 instrument_fail=1 own_fail=1`, `broken=1`, exit 1 | exit 0 — survives (reads manifest+capture, not the entry) | exit 0 | **KILLED** by harness AND audit |
| (d) | entry file deleted (`ls` → exit 2; knowledge files 49→48) | file absent | **FAIL** `problems=missing-entry` (row id + path printed, no traceback), `entries=23 pass=22 exit=1` | **FAIL** `lines=48 total=48`, `expected=49 missing=1 unexpected=0`, `missing_entries=[corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md]`, exit 1 | exit 0 — survives (manifest+capture intact) | exit 0 | **KILLED** by harness AND audit |

Item-level failure signatures, as assigned: (a) harness `pass=22` (< 23) and `exit=1`; (c) harness `pass=22
exit=1` + audit `parse_fail=1 exit=1`; (d) harness `pass=22 exit=1` + audit `missing=1 exit=1`. (b)/(b2) produced
**no** failure signature in any committed instrument — see §4.

## 4. The surviving mutant — coverage finding (recorded, not acted on)

`verified-at:` malformation survives the whole committed C2 instrument set, for two independent malformation
classes (invalid calendar date `2026-13-45`; placeholder `pending`). Measured basis:

- `grep -rn 'verified-at' corpus/instruments/*.py corpus/instruments/*.sh` → no hit in any instrument's code
  (the only occurrence in `corpus/instruments/` is inside a selftest fixture entry,
  `limb-fixtures/fr-duplicate-entry/corpus/knowledge/dup-entry.md`, which is data, not logic). The harness parses
  only `source:`/evidence/`recheck:` lines; the audit parses only the `recheck:` line and the expected-list;
  `source-recheck.py` reads only the manifest + capture; `capture-binding-check.py` reads only manifests +
  `SOURCES.md` (its strict-UTC `fetched_utc` rule covers manifest records, not entry headers).
- The asymmetry is real, not incidental: the same malformation class on a **manifest** (`fetched_utc: pending`)
  is instrument-rejected (`FAIL rule=fetched-utc … detail=pending`, `ExecManifestChecks` control C3/C-class), while
  the same class on the **entry header** is instrument-invisible.
- Where the field *is* enforced today: QUALITY Q1 ("`verified-at:` (ISO date the author re-opened it)") and the
  C2 kill rule's "entry … failing Q1-Q6" — both reviewer/judge-side (`RevEntryF20` §2 checks the Q1 header shape
  of the plan). So the claim is not unprotected, but its `verified-at` leg has no instrument-level detector: a
  future entry that lands with a malformed `verified-at:` passes `entries=23 pass=23 exit=0`,
  `expected=49 missing=0 unexpected=0`, `source-recheck exit 0` and `records=44 bound=44 unbound=0` until a human
  reads the header.

Per the mutation-tester protocol this is a coverage finding only — no instrument, entry, QUALITY row or claim was
changed by this seat.

## 5. Restoration evidence

After every mutation the pristine mirror bytes were restored from a copy kept outside the mirror and re-verified:

| after mutant | restored sha256 | harness re-run |
|---|---|---|
| (a) | `7b2214bf2108c01d8ad723f74d355db9e2f6cbc24b55e5592c1e2b04d87f2b0c` | `entries=23 pass=23 exit=0` |
| (b) | `7b2214bf2108c01d8ad723f74d355db9e2f6cbc24b55e5592c1e2b04d87f2b0c` | (verified at the (b2) cycle and finally) |
| (c) | `7b2214bf2108c01d8ad723f74d355db9e2f6cbc24b55e5592c1e2b04d87f2b0c` | `entries=23 pass=23 exit=0` |
| (d) | `7b2214bf2108c01d8ad723f74d355db9e2f6cbc24b55e5592c1e2b04d87f2b0c` | final full re-run below |

Final pristine re-verification on the restored mirror (all four instruments):

```text
harness         entries=23 pass=23 exit=0
audit           strict pass=49/49 … expect=present expected=49 missing=0 unexpected=0 exit=0
source-recheck  S054:sha256 OK; Q1..Q4 OK (anchors 259/277/473/68)  exit=0
capture-binding records=44 bound=44 unbound=0                       exit=0
```

Lane-side restoration: this seat wrote nothing into the lane except this receipt. `git status --porcelain` at the
end shows the same untracked `.ufo/waves/round-37/…` entries present at spawn and no `corpus/` entry; the one
modified path (`.ufo/waves/round-36/wave1/ScribeConsiderthese.md`) is a concurrent sibling's receipt write, not
this seat's. No mutating git/jj command was run (only `rev-parse`, `status`, `log`, `ls-tree`, `diff`, `archive`).

## 6. Transcripts (distinctive lines per mutant)

```text
(a) harness : FAIL  F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S053 exit=-    problems=header-sources-not-rechecked,selection-not-declared-by-entry
    harness : entries=23 pass=22 exit=1
    harness json: declared_ids=[S053] cited_ids=[S052,S053,S054] recheck_ids=[S054] exit=null
    audit   : strict pass=49/49 … expect=present expected=49 missing=0 unexpected=0 exit=0   (survives)
    src-rch : exit=0                                                                          (survives)

(b)  harness: entries=23 pass=23 exit=0   (PASS F20 ids=S054)      ← survives
     audit : lines=49 total=49 pass=49 … expect=present expected=49 missing=0 unexpected=0 exit=0   ← survives
     src-rch: exit=0   capture-binding: records=44 bound=44 unbound=0 exit=0                        ← survives
(b2) identical greens for `verified-at: pending` (placeholder class)                                ← survives

(c)  bash -n: syntax error near unexpected token `('  (exit 2)
     harness : FAIL  F20  … ids=S054 exit=-    problems=not-a-recheck-invocation,no-source-selection,no-manifest
     harness : entries=23 pass=22 exit=1
     audit   : strict pass=48/49 cdroot_fail=0 instrument_fail=1 own_fail=1
               executes=24 gated=24 broken=1 … parse_fail=1 cwd_fail=0 paths_fail=1 exit=1
     audit json: limbs parse=false cwd=true paths=false; strict instrument=false own=false; class=broken
     src-rch : exit=0   (survives — manifest+capture untouched)

(d)  harness : FAIL  F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=- exit=-    problems=missing-entry
     harness : entries=23 pass=22 exit=1
     audit   : strict pass=48/48 … lines=48 total=48 … exit=1
               expect=present expected=49 missing=1 unexpected=0 exit=1
     audit json: missing_entries=[corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md]
     src-rch : exit=0   (survives — manifest+capture intact)
```

Full transcripts and `--json` receipts were kept in the seat scratch (`receipts/pristine-*`, `mut-{a,b,b2,c,d}-*`,
`final-*`, `selftest-*`) and removed with the scratch after this receipt was written; the distinctive lines above
are copied verbatim from them.

## 7. Out-of-scope observations for the L1 (this seat changed nothing)

1. **Entry-note vs manifest anchor mismatch (cross-seat).** The planned entry's `recheck:` trailing comment
   predicts `Q1 … anchor=247-ok through Q4 … anchor=367-ok` (the entry-seat staged manifest,
   `39bfd72b…`, quotes 247/259/277/367), while the capture-seat manifest carrying the byte-exact landing
   instruction (`ExecC2Capture` §4, `fabc3163…`, 3989 B) pins 259/277/473/68. Both are self-consistent and both
   make every instrument green (this mirror used the capture-seat manifest per its landing instruction); the
   mismatch is comment-only and reaches no instrument verdict, but one of the two texts should be reconciled at
   integration so the entry's own note describes the manifest that actually lands. `ScribeRowS054` §8.3 flagged
   the same fork.
2. **Mirror-adaptation caveat carried from `ExecC2Harness` §6:** with the planned absolute-cd line unadapted, the
   harness's F20 record measures the live lane (`recheck-exit-2` pre-landing). After the L1 lands the round-37
   capture, the unadapted line goes green in-lane; the mirror adaptation used here exists only for the
   pre-landing mutation test and lands nowhere.
3. **(b) coverage gap** (§4) is the actionable finding: if instrument-level `verified-at` enforcement is wanted, it
   is a new check to be routed by the L1 — not something this seat could add within its write scope.

## 8. Scope, tooling, cleanup

- Writes: this receipt only (`.ufo/waves/round-37/wave1/MutC2Entry.md`). Scratch
  `/fast/scratch/hyaku/kasegi-r37/MutC2Entry/` (mirror, extracted artifact blocks, fetch, receipts) was removed
  after this receipt was copied into the wave dir; nothing scratch-borne remains outside this file.
- No tool was installed or upgraded; no pacman transaction (paused host-wide); no network install. Used the lane's
  committed instruments plus host `python3` 3.14 / `git` 2.56 / coreutils. One live fetch with the lane's
  `capture-source.py` (UA `kasegi-shokunin/1.0 (documentation capture; …)`) to reproduce the pinned capture bytes.
- No `agent://all` message; one coordination ack to `agent://KasegiR37` (erratum-1 applied). One read-only spec
  dump of nine sibling item prompts into scratch for artifact extraction.
- One invalid attempt is disclosed for honesty: the first (b) run asserted `count==1` on a string that occurs
  twice in the entry (header + L83 prose mention), aborted without writing, and the instrument runs that followed
  in that block therefore measured pristine bytes — discarded, and (b) was redone line-scoped (§3).

Report: `.ufo/waves/round-37/wave1/MutC2Entry.md`
