# ExecI11KillRule — round-41 wave-1 receipt (C1 I11 escape-state fixture specs)

Seat: `ExecI11KillRule` (executor, leaf). Item: convert the committed
CritKillRule escape states into precise, reproducible fixture specs the
round-41 suite's I11 selftest can construct in scratch.

Axes touched: **depth:verifiability** (primary), **coverage**.
No lane, fleet, or source-tree file was edited. No subagents dispatched (the
one permitted labrat probe was not needed). No tool installs. No network
fetches. Read-only git only; no mutating git/jj anywhere except inside a
throwaway `git init` fixture repo under the seat scratch (toplevel asserted
before every commit, per the host guard).

Deliverable: `.ufo/waves/round-41/wave1/ExecI11KillRule.fixtures.txt` —
216 lines, sha256 `a9efd1a9511098c013c5bde0e382dfca13680af097d89865ffdaa03bd4526653`.

---

## 1. L1 freeze corrections logged (authoritative, from wave1/CORRECTIONS-L1.md)

1. **BASE HASH.** The real round-41 base is the 40-char
   `5b29ea1439450f712581edf5f0f0bf98dfb262ab`; the 38-char literal in my
   dispatched prompt is unresolvable. Any `--export-ref <base>` /
   `git archive <base>` must use the 40-char form, and an unresolvable
   `--export-ref` must be reported as a distinct red (`ref-not-found` in the
   payload), never as a vacuous `closed<12/12 exit=1`.
   Verified against the lane repo (the `^{commit}` suffix must be quoted or the
   shell eats the braces):
   ```
   $ git rev-parse --verify "5b29ea1439450f712581edf5f0f0bf98dfb262ab^{commit}"
   5b29ea1439450b712581edf5f0f0bf98dfb262ab      # exit 0
   $ git rev-parse --verify "5b29ea1439450b712581edf5f0bf98dfb262ab"
   fatal: Needed a single revision                 # exit 128 — unresolvable
   ```
   The 40-char form is the commit `round-40 verifier spot-check (integrator,
   hyaku): non-author admit/reject`; the 38-char literal in my dispatched
   prompt resolves to nothing.
   *Note for the L1:* the live `claims.json` was re-read after this pass and
   now already carries the 40-char form plus an `errata` entry recording this
   exact correction (found_by ScribeShonenLog) — so the hash correction is
   landed; see §5.1 for the one residual wording item.
2. **I11 ESCAPE COUNT.** `.ufo/waves/round-40/wave2/CritKillRule.md` carries
   **EIGHT** `### F` escape states (F1-F8), not seven; the file's own intro
   prose ("7 distinct escape states reproduced") is the typo. The committed
   headings are authoritative. My fixture spec therefore covers **all eight**
   (F1-F8), and the I11 payload must read `escapes=8` and `red=8`, naming
   F1-F8.
   Verified against the committed bytes:
   `grep -c '^### F' .ufo/waves/round-40/wave2/CritKillRule.md` → **8**
   (headings at lines 41, 58, 80, 94, 107, 127, 142, 152).

**Correction to the L1 note's phrasing.** The note says "your seven fixture
specs must cover all eight". The committed file's own structure explains the
discrepancy and it matters for the deliverable's shape: the *scout* table
(`ScoutKillRuleSpec.txt`) merged F1 and F2 into one entry on the grounds that
section 4 of the committed file gives them a single combined correction
bullet, yielding "seven". That merge is a scout-side reading, not a property
of the committed bytes. Since the L1 requires `escapes=8 red=8 naming F1-F8`,
**the deliverable emits eight separate, individually addressable fixture
specs (F1-F8)**, each with its own setup, RED assertion and honest control —
so F1 and F2 are separately constructible and separately red. The combined
*fix* (recursive scan + clean-chain tolerance) is shared, but the fixtures
are not merged.

---

## 2. Reading notes — what the committed bytes actually say

Source of truth read in full:
- `.ufo/waves/round-40/wave2/CritKillRule.md` (8 `### F` states, §2; §3
  positive reproductions; §4 smallest safe corrections; §5 hygiene)
- `.ufo/waves/round-40/wave2/CritKillRule.pending-variants.md` (F7's five
  byte variants + the control)
- `.ufo/waves/round-40/wave2/CritKillRule.worktree-clean.sh` (F8's mechanism)
- `.ufo/waves/round-40/wave2/CritKillRule.h6-escapes.sh` (the committed H6
  limb, byte-copied, plus its scenario matrix)
- `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` (T2/T4/T7/T13/T14 —
  the sibling defeat-fixture format my specs mirror)
- `.ufo/waves/round-40/claims.json` (the C1 kill rule that F1-F8 escape:
  "any leftover kasegi-r39*/r40 scratch entry at filing other than the
  passed --work dir", `grep -c '⟨pending' corpus/lessons/round-40.md`,
  "lane working tree not clean at filing")
- `.ufo/waves/round-41/claims.json` (the frozen C1 predicate: I11 = "each of
  the seven committed CritKillRule escape states reds the limb it escapes";
  and the C1 kill rule's own tail: "the lane working tree not clean at
  filing; any `kasegi-r41*` scratch sibling at filing other than the passed
  --work dir")
- `corpus/instruments/r40-closure.sh` at `c7aea5e` (the committed `check_h6`
  limb, extracted verbatim to scratch for the probes)
- `.ufo/waves/round-41/wave1/ScoutKillRuleSpec.txt` (the scout table; used
  as a cross-check, corrected where it merged F1/F2)

### The committed H6 limb (verbatim, `git show c7aea5e:corpus/instruments/r40-closure.sh`)

```bash
check_h6() { # TREE REF
  local root=$SCRATCH_ROOT
  local realw='' realroot='' e b r out
  local strays=0 read=ok
  ...
  realw=$( cd "$WORK" 2>/dev/null && pwd -P ) || { printf 'strays=0,read=fail'; return 1; }
  if [ -d "$root" ]; then
    ...
    if ! out=$(find "$realroot" -mindepth 1 -maxdepth 1 -print 2>/dev/null); then
      printf 'strays=0,read=fail'; return 1
    fi
    while IFS= read -r e; do
      ...
      b=${e##*/}
      case $b in
        kasegi-r39*|kasegi-r40*) ;;
        *) continue ;;
      esac
      r=$( cd "$e" 2>/dev/null && pwd -P ) || { read=fail; continue; }
      case $realw in
        "$r"|"$r"/*) continue ;;
      esac
      strays=$((strays + 1))
    done <<< "$out"
  fi
  printf 'strays=%s,read=%s' "$strays" "$read"
  [ "$read" = ok ] && [ "$strays" -eq 0 ] && return 0
  return 1
}
```

Five structural defects are visible in those bytes and each maps to one
escape state: `find -mindepth 1 -maxdepth 1` (depth, F1/F2); the family
`case` is byte-literal and case-sensitive with no dot stripping (F3, F4);
the tolerance `case $realw in "$r"|"$r"/*` is a raw path prefix with no
clean-chain check (F5); the whole scan is guarded by `if [ -d "$root" ]`
(fail-open, F6). F7 and F8 escape clauses that live *outside* the suite
(the pending-marker grep and the filing-time `git status --porcelain`).

### Limb attribution (which round-41 limb each escape state must red)

| State | Committed clause escaped | Round-41 limb that must red | Evidence the fixed limb must produce |
|---|---|---|---|
| F1 nested leftover | "any leftover kasegi-r39*/r40 scratch entry" | **I6** (scratch-scan family, recursive depth) | `strays=1,read=ok` closed=0 |
| F2 work-inside-family container | same clause, but only as a predicate of invocation geometry | **I6** (recursive + clean-chain tolerance) | `strays=2,read=ok` closed=0 (>=1 mandatory) |
| F3 dotfile dir | same clause (leading dot not stripped) | **I6** (dot-prefixed entries included) | `strays=1,read=ok` closed=0 |
| F4 case / Unicode-separator | same clause (byte-literal, case-sensitive) | **I6** (case- and separator-insensitive) | `strays=3,read=ok` closed=0 (all three variants counted) |
| F5 ancestor-prefix tolerance | same clause (raw path prefix, no clean chain) | **I6** (readlink-canonicalised work-dir exclusion; same canonicalisation discipline as **I5**) | `strays=1,read=ok` closed=0 |
| F6 fail-open scan root | same clause (missing root = scan error treated as clean) | **I6** (fail-closed on scan error) | `strays=0,read=fail` closed=0 |
| F7 pending-marker respelling | `grep -c '⟨pending' corpus/lessons/round-40.md` | pending-marker clause over the round lesson (`corpus/lessons/round-41.md` in the export) | `pending=1,read=ok` closed=0, per variant |
| F8 git-status blindness | "lane working tree not clean at filing" (`git -C <lane> status --porcelain`) | working-tree-clean clause | `flags=1,dirty=0,ignored=0` (skip-worktree / assume-unchanged); `flags=0,dirty=0,ignored=1` (gitignored untracked); closed=0 |

**Note for the L1 / ExecSuiteCore:** the frozen C1 predicate assigns I5 to
*declared-block* path canonicalisation under the export root and I6 to the
*scratch* scan. F5's escape is a **scratch-side** canonicalisation defect
(tolerating a family entry that resolves to any ancestor of `--work`), so it
reds **I6**, not I5 — the T7 symlink-out-of-export defeat fixture is what
reds I5, and that is a separate fixture family. I have recorded F5's
affinity to the I5 canonicalisation discipline in the deliverable without
mis-attributing the limb.

**Open question for the L1 — RESOLVED (see §7).** The frozen predicate
enumerates I1-I12 and gives I11 the job "each of the seven committed
CritKillRule escape states reds the limb it escapes". Two of the eight
states — F7 and F8 — escape clauses that the round-41 suite as specified
(I1-I12) does **not** obviously own: F7's pending-marker clause was a
round-40 *kill-rule* clause over `corpus/lessons/round-40.md` (the round-41
analogue is `corpus/lessons/round-41.md`), and F8's clause is a *filing-time*
`git status --porcelain` gate enforced outside the instrument. The
deliverable therefore states the RED assertion each of the two clauses must
produce, on the reading that I11 constructs both states in scratch and
asserts both clauses red — the reading this deliverable's aggregate payload
`escapes=8,red=8,F1=red..F8=red` assumes. I did not widen the frozen I1-I12
enumeration myself: that is the L1's call and it is not a seat-level change.
**The L1 confirmed this reading and assigned F7 and F8 to I11** (§7).

---

## 3. The deliverable

`.ufo/waves/round-41/wave1/ExecI11KillRule.fixtures.txt` — 216 lines,
sha256 `a9efd1a9511098c013c5bde0e382dfca13680af097d89865ffdaa03bd4526653`.

It contains **only** the landable fixture-spec bytes (no validation tables,
no notes, no receipt material): eight fixture blocks F1-F8, each with the
five required elements — (1) the name, (2) the exact sandbox setup commands,
(3) the limb it escapes, (4) the RED assertion the fixed limb must produce
with payload values, (5) the honest control that stays green — plus a closing
block stating the I11 aggregate payload and the graded selftest line shape.
Every fixture also names the RED payload values in the `strays=`/`read=` /
`pending=` / `flags=` vocabulary the fixed limbs must use, and states the
mandatory property in parentheses wherever a conforming implementation may
legitimately differ (only the F2 container count can differ).

Three extra controls/variants are included where they pin the escape
mechanism rather than restating the red case: F3's no-dot counterpart (the
match must not be dot-dependent), F5's symlink-directly-to-work control and
its real-directory-plus-junk variant, F6's non-directory-root variant, F4's
three-variant count, and F7's five byte variants.

---

## 4. Validation evidence (commands run, actual output)

All work under `S=/fast/scratch/hyaku/kasegi-r41/ExecI11KillRule` (removed
before yield). Disk guard green before and after
(`/fast/scratch/hyaku 24%, 610.4G free`).

### 4.1 The eight escapes reproduce against the COMMITTED round-40 limb

Committed limb extracted verbatim (`git show c7aea5ef97902f38289cbdc1cf267068876a62dd:corpus/instruments/r40-closure.sh`)
and sourced in scratch; the family names are the round-40 spellings
(`kasegi-r40*`) since that is the limb under test.

```
$ bash probe.sh   # section A
case=F1 nested leftover (r40)           expect=green rc=0 payload=strays=0,read=ok  verdict=pass
case=F3 dotfile dir (r40)               expect=green rc=0 payload=strays=0,read=ok  verdict=pass
case=F4 case+separator (r40)            expect=green rc=0 payload=strays=0,read=ok  verdict=pass
case=F5 ancestor-prefix link (r40)      expect=green rc=0 payload=strays=0,read=ok  verdict=pass
case=F6 missing scratch root (r40)      expect=green rc=0 payload=strays=0,read=ok  verdict=pass
```

F2 and F5 confirmed against the committed limb separately (the r40-family
equivalents of the round-41 states):

```
$ bash probe4.sh
=== F2 escape against the COMMITTED r40 H6 limb (r40 family names) ===
F2 committed: rc=0 payload=strays=0,read=ok (expected green: nested leftover invisible)
=== F5 escape against the COMMITTED r40 H6 limb ===
F5 committed: rc=0 payload=strays=0,read=ok (expected green: ancestor-prefix tolerated)
```

### 4.2 F7 and F8 reproduce against the committed clauses

F7 — the committed round-40 filing clause (`grep -c '⟨pending'`) vs. a
normalized marker class:

```
$ bash probe2.sh   # section F7
variant=canonical r40-clause rc=1 payload=pending=1,read=ok | fixed rc=1 payload=pending=1,read=ok
variant=space     r40-clause rc=0 payload=pending=0,read=ok | fixed rc=1 payload=pending=1,read=ok
variant=u2329     r40-clause rc=0 payload=pending=0,read=ok | fixed rc=1 payload=pending=1,read=ok
variant=ascii     r40-clause rc=0 payload=pending=0,read=ok | fixed rc=1 payload=pending=1,read=ok
variant=case      r40-clause rc=0 payload=pending=0,read=ok | fixed rc=1 payload=pending=1,read=ok
variant=upper     r40-clause rc=0 payload=pending=0,read=ok | fixed rc=1 payload=pending=1,read=ok
variant=clean     r40-clause rc=0 payload=pending=0,read=ok | fixed rc=0 payload=pending=0,read=ok
```

F8 — the committed filing clause (`git status --porcelain`) vs. a clause that
also reads `git ls-files -v` flags and the ignored-untracked set:

```
$ bash probe3.sh
  clean repo (honest control)             r40-clause rc=0 payload=dirty=0 | fixed rc=0 payload=flags=0,ignored=0,dirty=0
  (a) skip-worktree hides tracked change  r40-clause rc=0 payload=dirty=0 | fixed rc=1 payload=flags=1,ignored=0,dirty=0
  (a2) assume-unchanged hides tracked change r40-clause rc=0 payload=dirty=0 | fixed rc=1 payload=flags=1,ignored=0,dirty=0
  (b) gitignore hides untracked file      r40-clause rc=0 payload=dirty=0 | fixed rc=1 payload=flags=0,ignored=1,dirty=0
  visible dirty (control)                 r40-clause rc=1 payload=dirty=1 | fixed rc=1 payload=flags=0,ignored=0,dirty=1
```

(The F8 fixture repo is created with `git -C "$D" init -q` and the host-guard
assertion `[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]` is checked
before every commit; the throwaway identity is passed per-command with
`-c user.name=t -c user.email=t@t`, never written to any config file.)

### 4.3 Every fixture and control in the deliverable executes as specified

`validate.sh` runs each of the eight fixtures and their honest controls
against reference fixed limbs and compares the payload and exit code to the
values written in the deliverable:

```
$ bash validate.sh
== F1 nested leftover ==
  F1 red                             expect rc=1 payload=strays=1,read=ok                | got rc=1 payload=strays=1,read=ok                pass
  F1 control                         expect rc=0 payload=strays=0,read=ok                | got rc=0 payload=strays=0,read=ok                pass
== F2 work inside family container ==
  F2 red                             expect rc=1 payload=strays=2,read=ok                | got rc=1 payload=strays=2,read=ok                pass
  F2 control                         expect rc=0 payload=strays=0,read=ok                | got rc=0 payload=strays=0,read=ok                pass
== F3 dotfile ==
  F3 red                             expect rc=1 payload=strays=1,read=ok                | got rc=1 payload=strays=1,read=ok                pass
  F3 control                         expect rc=0 payload=strays=0,read=ok                | got rc=0 payload=strays=0,read=ok                pass
  F3 no-dot counterpart              expect rc=1 payload=strays=1,read=ok                | got rc=1 payload=strays=1,read=ok                pass
== F4 case/separator ==
  F4 red                             expect rc=1 payload=strays=3,read=ok                | got rc=1 payload=strays=3,read=ok                pass
  F4 control                         expect rc=0 payload=strays=0,read=ok                | got rc=0 payload=strays=0,read=ok                pass
== F5 ancestor-prefix tolerance ==
  F5 red                             expect rc=1 payload=strays=1,read=ok                | got rc=1 payload=strays=1,read=ok                pass
  F5 control                         expect rc=0 payload=strays=0,read=ok                | got rc=0 payload=strays=0,read=ok                pass
  F5 variant dir+junk                expect rc=1 payload=strays=1,read=ok                | got rc=1 payload=strays=1,read=ok                pass
== F6 fail-open scan root ==
  F6 red (missing root)              expect rc=1 payload=strays=0,read=fail              | got rc=1 payload=strays=0,read=fail              pass
  F6 control (empty root)            expect rc=0 payload=strays=0,read=ok                | got rc=0 payload=strays=0,read=ok                pass
  F6 variant (file root)             expect rc=1 payload=strays=0,read=fail              | got rc=1 payload=strays=0,read=fail              pass
== F7 pending marker class ==
  F7 red (space)                     expect rc=1 payload=pending=1,read=ok               | got rc=1 payload=pending=1,read=ok               pass
  F7 red (u2329)                     expect rc=1 payload=pending=1,read=ok               | got rc=1 payload=pending=1,read=ok               pass
  F7 red (ascii)                     expect rc=1 payload=pending=1,read=ok               | got rc=1 payload=pending=1,read=ok               pass
  F7 red (case)                      expect rc=1 payload=pending=1,read=ok               | got rc=1 payload=pending=1,read=ok               pass
  F7 red (upper)                     expect rc=1 payload=pending=1,read=ok               | got rc=1 payload=pending=1,read=ok               pass
  F7 control                         expect rc=0 payload=pending=0,read=ok               | got rc=0 payload=pending=0,read=ok               pass
== F8 working-tree clean ==
  F8 control (clean repo)            expect rc=0 payload=flags=0,dirty=0,ignored=0       | got rc=0 payload=flags=0,dirty=0,ignored=0       pass
  F8 red (skip-worktree)             expect rc=1 payload=flags=1,dirty=0,ignored=0       | got rc=1 payload=flags=1,dirty=0,ignored=0       pass
  F8 red (assume-unchanged)          expect rc=1 payload=flags=1,dirty=0,ignored=0       | got rc=1 payload=flags=1,dirty=0,ignored=0       pass
  F8 red (gitignored untracked)      expect rc=1 payload=flags=0,dirty=0,ignored=1       | got rc=1 payload=flags=0,dirty=0,ignored=1       pass

validation: pass=25 fail=0
```

The reference fixed limbs used for validation (`fixed-scan.sh`,
`scan_pending_fixed`, `scan_wt`) live in the seat scratch and are **not**
deliverables — they are the harness that proves the fixture specs are
constructible and produce the stated payloads; the suite author implements
the real limbs.

---

## 5. Risks and open items for the L1

1. **The live `claims.json` has already been corrected in place by the L1**
   (re-read after my first pass). It now carries `"base":
   "5b29ea1439450b712581edf5f0f0bf98dfb262ab"`, the 40-char literal in the
   C1 `counting_commands` and predicate prose, and an `errata` array with two
   entries (found_by ScribeShonenLog): the base-hash literal and the I11
   escape-state count — the latter recording exactly the correction I
   implemented ("I11's target is the eight committed states; I11 payload must
   read escapes=8 and red=8, naming F1-F8"). **No reconciliation action is
   outstanding on the base hash**; my §1.1 note is superseded by this
   re-read.
2. **Residual wording mismatch in the live claims.json — CLOSED by the L1.**
   The `errata` entry records the eight-state correction, but the C1
   `predicate` prose still reads "I11 each of the seven committed
   CritKillRule escape states reds the limb it escapes" and the C1
   `kill_rule` still reads "the CritKillRule seven escape states". The L1's
   ruling (§7): the predicate text stays frozen and the `errata` block binds
   I11 to the eight committed states F1-F8 — the same class as the base-hash
   fix (a frozen body plus a binding erratum). My deliverable implements
   the erratum (eight specs, `escapes=8 red=8`). No further action.
3. **F7 and F8 limb ownership — CLOSED by the L1.** Both are assigned to
   **I11**: F7 via a pending-marker clause on `corpus/lessons/round-41.md`
   (`⟨pending` count = 0), F8 via a worktree-clean clause reading
   `git status --porcelain` with ignore/skip-worktree semantics
   (`flags=1` / `ignored=1` payloads, per my §4.2 evidence). The L1 has
   notified ExecSuiteCore. The deliverable's payloads match that assignment.
4. **F2's exact count.** An implementation that tolerates any ancestor of
   `--work` counts 1 where the clean-chain implementation counts 2. The
   fixture states `strays=2` and marks `strays>=1` as the mandatory
   property, so it reds under either reading while still pinning the
   reference behaviour.
5. **The suite's family spelling.** My specs use the round-41 family
   (`kasegi-r41*`, case/separator/dot-insensitive) per the frozen I6 text.
   If ExecSuiteCore's limb normalises separators to `_` rather than `-`, the
   F4 variant names in the deliverable remain valid (they are inputs, not
   expectations), but the F4 *control* name `kasegi-r40-stray` and the F3/F5
   family names must be re-checked against the final matcher — they are
   out-of-family names, so any round-41 matcher keeps them green.

## 6. Hygiene

- Disk guard green before and after the work.
- No tool installed or upgraded; no pacman; no network fetch.
- No write to `~/.local/bin` or any PATH directory; no fleet-root tracked
  file touched; no lane file edited beyond the two files this seat names
  (receipt + deliverable) under `.ufo/waves/round-41/wave1/`.
- No mutating git/jj in the lane, fleet or any source tree; the only commits
  are inside the throwaway fixture repo under the seat scratch, with the
  toplevel assertion checked first.
- Seat scratch `/fast/scratch/hyaku/kasegi-r41/ExecI11KillRule/` removed
  before yield; no `kasegi-r41*` sibling survives from this seat.

## 7. L1 confirmation (after first yield) — both open items closed

The L1 (agent `KasegiR41`) confirmed this seat's analysis and closed both
open items. Recorded here so the receipt carries the final state.

1. **F7 / F8 ownership — assigned to I11.** I11 constructs all eight
   committed states: F1-F6 red via the shared **I6** scratch-scan limb; F7
   via a pending-marker clause on `corpus/lessons/round-41.md` (`⟨pending`
   count = 0); F8 via a worktree-clean clause reading `git status --porcelain`
   with ignore/skip-worktree semantics (`flags=1` / `ignored=1` payloads, per
   my §4.2 evidence). The L1 has notified ExecSuiteCore. This matches the
   reading my deliverable encodes (I11 constructs and asserts all eight), so
   the deliverable's payloads require no change.
2. **claims.json predicate text — stays frozen; the `errata` block binds.**
   The errata entry (already present in the live file) binds I11 to the eight
   committed states F1-F8, the same class as the base-hash fix: a frozen body
   plus a binding erratum. No re-wording of the predicate is required, and
   none is requested of this seat.
3. **Separate-fixtures reading confirmed.** The L1 affirmed that F1 and F2
   are not merged: my eight-spec deliverable (one spec per committed `### F`
   heading) is the required shape, since the payload must name F1-F8
   individually and each must be separately constructible and separately red.
   The shared *fix* (recursive scan + clean-chain tolerance) does not imply a
   merged *fixture*.
4. **F5 re-attribution to I6 recorded** by the L1.

**No further action on this seat.** The deliverable
(`ExecI11KillRule.fixtures.txt`, 216 lines, sha256
`a9efd1a9511098c013c5bde0e382dfca13680af097d89865ffdaa03bd4526653`) stands as
the I11 fixture spec. The two items above changed no byte of the deliverable;
only this receipt was updated, to replace "awaiting an L1 decision" framing
with the decision itself.
