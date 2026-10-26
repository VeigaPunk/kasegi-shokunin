# SimplC1 — round-37 hygiene audit (evidence size, scratch, /tmp, duplicate content, disk guard)

Seat: SimplC1 · lane `kasegi-shokunin` · round 37 · axis depth:verifiability · read-only audit.
Lane HEAD at read: `b362068195d5489aa94b31e6ec8f880c367e0ba0`; round-37 worktree untracked-only
(`git status --porcelain`: 52 entries, all under `.ufo/waves/round-37/`), no tracked file modified.
Snapshot times below are 2026-10-26, local 14:12–14:22 / UTC 17:12–17:22. Receipt is written last;
my scratch `/fast/scratch/hyaku/kasegi-r37/SimplC1/` is removed before yield.

Write scope respected: this receipt plus scratch only. No lane/fleet/sibling write, no mutating git,
no pacman (host transactions paused), no tool installs (nothing needed; recorded as none).

---

## 1. Disk-guard status check (driver instrument, read-only invocations)

```
$ cd /home/vgpnk/Projects/shokunin && bash scripts/hyaku/disk-guard.sh status   # rc=0
root                             use%     free
/tmp                               3%   125.3G
/var/tmp                          35%   582.4G
/fast/scratch/hyaku               28%   584.5G
(top consumers: /fast/scratch/hyaku/souji-r33 22.8G, tameshi-r48 8.0G, kengaku-r40 5.7G,
 kasegi-r37 2.4G→4.3G live, tabi-r32 1.2G; /tmp/.mount_appimap0T6hX 363.1M; other lanes' /tmp,
 /var/tmp fixtures)

$ bash scripts/hyaku/disk-guard.sh check    # rc=0
ok root=/tmp use=3% soft=70%
ok root=/var/tmp use=35% soft=70%
ok root=/fast/scratch/hyaku use=30% soft=70%
check_rc=0

$ bash scripts/hyaku/disk-guard.sh selftest # rc=0
selftest_rc=0
```

Thresholds are the `hyaku.env` values, not defaults: `SOFT_PCT=70 TARGET_PCT=60 HARD_PCT=90
IDLE_MIN=45 MIN_AGE_MIN=10`, roots `/tmp /var/tmp /fast/scratch/hyaku`. Every root sits **≥ 40
percentage points below SOFT**; no root is near pressure, and the gate's own seeded-defect arm
proves it can fail (`selftest` rc 0). **No disk pressure on this round's lane.**

Two instrument facts a seat must know before it quotes this:

1. `check` is **not read-only**. `cmd_check` calls `log_line` for every root
   (`scripts/hyaku/disk-guard.sh:531-541`), so it appends to the driver-owned append-only
   `$FLEET/.ufo/state/disk-guard.log` — a fleet-root write. My run added exactly three lines at
   `2026-10-26T17:15:15Z ok /tmp|/var/tmp|/fast/scratch/hyaku` (grep count 3); the adjacent
   `17:14:53Z` and `17:15:25Z` triplets belong to other callers. `status` has no `log_line` call
   and writes nothing. A seat that must honour "fleet root is read-only" should use `status`,
   never `check`/`sweep`. Recorded, not corrected (the log is driver-owned).
2. `kasegi-r36` still exists at `/fast/scratch/hyaku/kasegi-r36` (0 B, idle=59 min at read).
   Round-36's round-close `purge-lane` did not remove its own root; it is sweep-eligible
   (idle > IDLE_MIN 45, size 0) and `purge-lane kasegi 36` removes it. Outside my write scope —
   listed as a cleanup candidate for the driver, not deleted.

## 2. Wave evidence size (nothing near the gate)

| measure | round-37 @ read | round-36 (committed, reference) |
|---|---|---|
| `.ufo/waves/round-37/` total | **57 files, 2,297,093 B (2.19 MiB)** | 2,668,477 B |
| `wave1/` files | 45 (44 receipts + `swarm-registry.json`), 884,346 B | 65 files, 1,209,543 B |
| largest file | `wave1-dispatch.json` **473,712 B** (tracked) | `wave1-dispatch.json` 372,309 B |
| largest receipt | `ExecC1SuiteBuild.md` **93,187 B** (live) | `ExecC1SuiteBuild.md` 75,534 B |
| files > 1 MiB | **0** in round-37 | 0 |
| files > 10 MiB | **0** anywhere in the worktree | — |

The commit gate is 10 MiB, not 1 MiB: `scripts/hyaku/jj-lane.sh:639`
`[ "$(stat -c %s -- "$q")" -gt 10485760 ] && err "named file over 10 MiB needs --allow-large: $q"`.
**No round-37 file needs `--allow-large`.** The seat prompt's ">1 MiB without `--allow-large`"
phrasing is 10× stricter than the instrument; if 1 MiB is the intended ceiling, the gate does not
enforce it. Recorded as a spec/instrument mismatch, not acted on.

Only two worktree files exceed 1 MiB, both **pre-existing tracked provenance captures** — do not
trim, they are the archived source bytes themselves:

```
1470121  .ufo/waves/round-29/wave1/assimilation/fetch/S069.pdf
1479694  corpus/source-snapshots/round-35/S052.txt
```

Projected round-37 addition still to land (suite 60 KB, S054 snapshot ~105 KB, lesson/LOG/SCORECARD
section, `final-gates/all-gates.txt` ~2–3 KB) keeps the round at or under round-36's committed total.

## 3. Scratch (all bound to `/fast/scratch/hyaku/kasegi-r37/<seat>`)

`/fast/scratch/hyaku/kasegi-r37` = **2.4 G at 17:07Z → 4.3 G at 17:15Z**, 27 seat dirs +
`l1prep/` + `build-spec.py`; every dir mtime ≤ 17 min at read (live round work trees, not
abandoned). Heavy consumers: `CritC2Kill` 2.1 G (lane copy `v/`), `ExecDatawalk` ~0.9 G (seven
~140 M mirror/rename fixtures), `CritMotivation` 772 M, `CritC2Claim` 390 M, `RevHarnessSync-2`
269 M, `ExecGateReviewPrep` 258 M, `CritBoundary` 147 M. Lane `.git` is 39 M, `.jj` 11 M, so the
multi-GB entries are seat work trees, not repo growth.

E9 consequence (from the quiescence seat's own sequencing, `wave1/ExecQuiescenceProbe.md:290-300`):
the suite's quiescence limb reads `scratch-seat-dirs=0`, so

1. commit every seat receipt + `wave1*` + `assimilation/*` (porcelain → 0),
2. run `--export-ref <that head> --work <outside the lane>` after **all seat dirs *and* `l1prep/`**
   are removed,
3. commit the resulting `final-gates/all-gates.txt` (it names its parent head by construction).

**This is the one cleanup list entry that can turn the round red by omission.** My own `SimplC1/`
dir is removed at yield.

Scratch-only artifact worth a decision: `/fast/scratch/hyaku/kasegi-r37/build-spec.py`
(55,290 B) is the round-37 dispatch builder, and it exists **only in scratch** while round-36
committed `.ufo/waves/round-36/build-spec.py` (45,920 B). After the purge the round-37 dispatch is
not reproducible from repo bytes. Minimal fix is one file (`git` commit of the builder, 55 KB) or a
recorded deliberate exclusion — the L1's call, not mine.

## 4. /tmp usage (no lane evidence depends on it)

`/tmp` 3 % (125.3 G free), `/var/tmp` 35 % (582.4 G) — no file over 50 MB in either, so the
/tmp-only-under-50-MB rule is not violated. Round-37 strays created after dispatch (13:55 local):

```
13:55 103289 /tmp/ssvc.html     13:55 103289 /tmp/ssvc2.html
13:55   6731 /tmp/ssvc3.html    13:55 105807 /tmp/ssvc4.html     # C2 source fetch working copies
14:06    265 /tmp/reg-now.txt                                    # cmp: byte-identical to assimilation/reg-ids
```

`/tmp/reg-now.txt` is an unbound scratch write (`cmp` silent against
`.ufo/waves/round-37/assimilation/reg-ids`). Root cause is mechanical: **`TMPDIR` is unset in this
seat's shell and `/fast/scratch/hyaku/tmp` does not exist**, although `hyaku.env` says to launch
with `TMPDIR=$HYAKU_SCRATCH/tmp`; seats using bare `mktemp` therefore land in `/tmp`. Fix is one
`mkdir -p /fast/scratch/hyaku/tmp` + exported `TMPDIR` at dispatch, or `mktemp -p "$S"` per seat.

No round-37 receipt cites `/tmp` (`grep -rn "/tmp/" wave1/*.md` → 0 hits) and 31 receipts cite the
bound scratch root only as command paths, so nothing dangles when scratch is purged. Unattributed
13:57–14:00 files (`/tmp/nwv_*.json`, `nw_gate.out`, `h.old/h.new`) are not kasegi-by-name and were
left alone.

## 5. Duplicate-content audit (nothing silently duplicated)

- Zero duplicate content hashes across the 45 wave1 files (`sha256sum wave1/* | uniq -d` empty).
- `wave1-spec.json` / `wave1-plan.out` / `wave1-dispatch.json` are three distinct digests —
  `1e201e64…`, `a42ca84a…`, `119f0883…` — not copies of one another.
- The three before-controls are distinct: `census-before.txt ada01b8e…`, `c1-controls/before.txt
  63670cf5…`, `c2-controls/before.txt fd849486…`.
- The only real re-implementation is the planned suite. Scratch build
  `/fast/scratch/hyaku/kasegi-r37/ExecC1SuiteBuild/r37-closure.sh` (1,333 lines / 60,028 B) vs
  committed `corpus/instruments/r36-closure.sh` (894 lines / 39,022 B): `check_e2/e4/e5/e6` bodies
  are **byte-identical** (sha256 prefix match), `check_e1/e3/e7/e8` differ only in round-37
  constants, `check_e9` is rewritten 37→50 lines (the fail-closed rewrite D6 requires). The header
  already names that provenance (lines 4–5: "E1-E9 carry the round-36 closure semantics (with E9
  rewritten fail-closed)"), so this is **documented** duplication, not a second undocumented
  authority. Do not delete either suite: E3 requires the `r36-closure.sh` registry row and the
  r36 suite is the negative-control fixture. Tradeoff recorded: four check bodies now live twice,
  so a future fix must land twice.
- Planned new paths are all absent at read (no overwrite, no same-basename collision):
  `corpus/instruments/r37-closure.sh`, `corpus/lessons/round-37.md`,
  `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`,
  `corpus/source-snapshots/round-37/`, `.ufo/waves/round-37/final-gates/`,
  `corpus/considerthese-ledger.md`, `.ufo/waves/round-37/c2-controls/junk-f20.md`.
  `corpus/knowledge/` holds 48 entries, none matching `ssvc|stakeholder`; `corpus/SOURCES.md` has
  no `S054` row yet — so the C2 knowledge entry and registry row are genuinely new, not duplicates.
- `c2-controls/junk-f20.md` is the negative-control twin (precedent: committed
  `.ufo/waves/round-36/c2-controls/junk-f19.md`). It must land **only** under `c2-controls/`; a
  copy under `corpus/knowledge/` would let the harness test its own committed ground.
- `assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}` total 1,267 B. They are derivable
  id dumps, but two receipts prove byte-identity by path (`ScoutIdCollisions.md:63`,
  `ScoutStandingRefusals.md:44-46`) and the quiescence seat's sequence requires committing
  `assimilation/*` for `porcelain → 0`. **Commit them (1.3 KB); deleting them would strand the
  byte-identity evidence and leave untracked paths that reopen E9.**
- No `.orig/.bak/*~/*.tmp/*.partial/*.rej` files anywhere in `.ufo/waves/round-37/`; no base-tree or
  fixture copies inside the lane worktree.
- **One tracked prior-round file is modified** (appeared between 14:12 and 14:18 local; absent from
  my first `-uall` scan): `.ufo/waves/round-36/wave1/ScribeConsiderthese.md` is `M` with +38 lines
  ("§ 8. Post-integration addendum (appended 2026-10-26T17:13Z, read at lane head `b362068`)"),
  `git diff --stat` = `1 file changed, 38 insertions(+)`, blob `217d29c → 520c603`. Round-36 wave1
  receipts are historical evidence; the round-36 lesson is the sanctioned correction site (E8), and
  this addendum carries corrections (§4 F-1/F-5 row-text correction) plus a mid-wave diagnostic. It
  is additive, timestamped, and states "sections 1–7 … left as written", but it was **not**
  pre-declared append-only, and it changes committed round-36 evidence bytes inside round 37.
  Decision for the L1, not mine: keep the append (and say so in the round-37 lesson/LOG) or move
  the text to the round-37 lesson/receipt and restore blob `217d29c`. Do not leave the choice
  implicit in a dirty tree — E9 reds on it, and a reviewer cannot tell append from edit.

## 6. Minimal cleanup list

**Must not be committed (delete from /tmp; none is lane content):**

1. `/tmp/reg-now.txt` — bound duplicate of `assimilation/reg-ids`.
2. `/tmp/ssvc.html`, `/tmp/ssvc2.html`, `/tmp/ssvc3.html`, `/tmp/ssvc4.html` — C2 fetch working
   copies; the committed form is the bound `corpus/source-snapshots/round-37/S054.txt` (+ manifest).
3. Nothing else: no scratch tree, fixture copy, or oversized stray exists inside the lane worktree.
4. **Hold the `M .ufo/waves/round-36/wave1/ScribeConsiderthese.md` hunk until the L1 decides its
   home** (§5, last bullet). It is not junk — it is +38 additive lines — but committing it as-is
   rewrites round-36 evidence bytes without a pre-declared append-only convention, and leaving it
   uncommitted keeps `git status` dirty so E9 reds.

**Must not be trimmed (provenance):**

- `S069.pdf` (1,470,121 B) and `S052.txt` (1,479,694 B) — archived source bytes.
- All wave1 files (max 93 KB each; 50 receipts + registry by the time this receipt was written), the three dispatch artefacts, the before-controls, and the
  1.3 KB assimilation working files — each is either cited by a receipt or needed for E9's
  `porcelain → 0`.

**Trim only at generation time:** `final-gates/all-gates.txt` should stay at round-36's shape
(1,203 B: digest header, 14 `E<n> payload=` lines, 14 `selftest case=` lines, totals, neg legs);
do not paste a full selftest transcript into it or into a receipt.

**Purge before the final gate (ordering, not discretion):**

- all 27 seat dirs **and `l1prep/`** under `/fast/scratch/hyaku/kasegi-r37/` (E9
  `scratch-seat-dirs=0`), then gate with `--work` outside the lane, then commit `all-gates.txt`;
- `/fast/scratch/hyaku/kasegi-r36/` (0 B leftover) via `purge-lane kasegi 36`.

## 7. Verdict

Disk guard green on all three roots (exit 0, selftest 0, ≥40 points of headroom); evidence size is
at parity with round-36 and nowhere near the 10 MiB gate; no duplicate content is being committed;
the only red-by-omission risk is scratch quiescence (27 seat dirs + `l1prep/` must be gone before
E9 runs). Two file decisions remain open: the scratch-only `build-spec.py` (land or record) and the
+38-line mutation of a committed round-36 receipt (keep or relocate + restore `217d29c`). Two
instrument notes are recorded rather than fixed (10 MiB vs 1 MiB gate wording; `check` logs into the
driver-owned fleet log while `status` does not), plus the unset-`TMPDIR` root cause behind the five
`/tmp` strays.

---

Scratch hygiene: `/fast/scratch/hyaku/kasegi-r37/SimplC1/` removed at yield. Tooling: none
installed or upgraded (no pacman, no `uv tool install`, no `npx`). Fleet-root writes attributable
to this seat: the three `disk-guard.log` `ok` lines at 17:15:15Z produced by the sanctioned
`check` command, disclosed in § 1.
