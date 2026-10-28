# R44Exec4 — C1 defect 6: SHONEN base/tip tail bytes and the exact blank-line delta

Assigned item: "Inspect SHONEN base/tip tail bytes and calculate exact blank-line difference read-only."
Frozen defect: `corpus/lessons/round-43-verifier-spotcheck.md` §6 item 6 (`SHONEN.md` lost one base byte, final empty line, in `0a24364d`; restore it at the next append).
Scope: read-only over committed bytes. No production/shared file edited, no git/jj/index mutation, no commit, no tools installed.

## 1. Measured answer — the delta is exactly one byte, at offset 30157

| revision | blob | bytes | newlines (`wc -l`) | blank lines (`grep -c '^$'`) | last 2 bytes | sha256 |
|---|---|---|---|---|---|---|
| base `ab98fac9` | `0bce289` | 30157 | 285 | **34** | `0a0a` | `153a87306502881b060804c11b6c0e08644101583894036803f8f60a5eec81e7` |
| `0a24364d` = `dbd2e106` = `fdc20ad6` = HEAD `6631401` | `f7c5072` | 34691 | 292 | **33** | `2e0a` | `e845b653ab23f1078867c76245d59985ee15848c68292f655a1a21e90d084740` |

- Base byte **30157 (1-based) = `0x0a`** — the newline terminating the base's final empty line (base `L285`, `length($0)==0`). At the tip, byte 30157 is **`0x2d`** (`-`), the first byte of the appended round-43 box.
  `git show ab98fac9:SHONEN.md | dd bs=1 skip=30156 count=1 | xxd` → `0a`; `git show HEAD:SHONEN.md | dd bs=1 skip=30156 count=6 | xxd` → `2d20 5b7e 5d20` (`- [~] `).
- **Prefix identity (decisive):** `sha256(base[1..30156]) == sha256(tip[1..30156]) == c29eee3c9d00b2ecb8a1fcc9cc8151bc11051c5f20663d4a8c829e6739a43d31`. The restore wrote the base bytes **minus the last `0x0a`**, then appended. Nothing else in the base range moved.
- **Arithmetic closes both ways:** `30157 − 1 + 4535 = 34691` (appended block = 8 lines / 4535 bytes, measured `git show HEAD:SHONEN.md | tail -n 8 | wc -c`); `285 − 1 + 8 = 292` newlines; `34 − 1 = 33` blank lines. Net: **+4534 B, +7 newlines, −1 blank line**.
- **Diff shape:** `git diff --numstat ab98fac9 dbd2e106 -- SHONEN.md` → `8 1`; `--stat` → `SHONEN.md | 9 ++++++++-`; the single deletion is the lone empty line in hunk `@@ -285 +285,8 @@` (raw `-` with `$` only, `git diff … | grep -n '^-'` → the only non-header match is `9:-$`).
- **No box changed:** `- [~]` lines 36 (base) → 40 (HEAD, +4 round-43 boxes); `- [x]` = 0 at both; the changed region is `L285..L292` only.

### Where the byte was lost
`git show <rev>:SHONEN.md | wc -c` / `tail -c 2 | xxd -p` per commit:

```
4cb6d4ae 30157 / 285 / 0a0a      (base bytes intact through the freeze commit)
5b4a8503 30157 / 285 / 0a0a
a6c1d462 30157 / 285 / 0a0a
ffe197d1 30157 / 285 / 0a0a
9e6800ea  4536 /   9 / 2e0a      (L1 f-string truncation: blob 0518fdde, only the 4 new boxes survive)
6c360f4c  4536 /   9 / 2e0a
0a24364d 34691 / 292 / 2e0a      (restore-and-reappend: blob f7c5072 — the loss happens here)
f2dee6c0 / 2448a7d2 / 2fccc781 / 3634ec94 / fdc20ad6 / dbd2e106 / 6631401 → 34691 / 292 / 2e0a (blob unchanged)
```

`git show --stat 0a24364d -- SHONEN.md` → `283 insertions(+)`; `git diff --numstat 0a24364d^ 0a24364d -- SHONEN.md` → `283 0` (the 9 truncated lines are a common prefix, so the restore reads as pure insertion — which is exactly why the lost blank line is invisible in that commit's own numstat).

## 2. Scope check — the loss is one file, one byte (bounded scan)

All 9 pre-existing files changed base→HEAD were tested for the discriminating property *"base full prefix differs, base-minus-one-byte prefix matches"*:

```
for f in $(git diff --name-only $B $H); do  # skip files absent at base
  cmp sha256(base[1..Bsz]) vs sha256(head[1..Bsz]); if differ, cmp sha256(base[1..Bsz-1]) vs sha256(head[1..Bsz-1])
done
→ MINUS1-PATTERN: SHONEN.md base=30157 head=34691 sha=c29eee3c9d00
→ scanned=9
```

`SHONEN.md` is the **only** match. The three other records whose last two bytes moved `0a0a → 2e0a` are *not* losses — their base final empty line survives as an interior line and the full base byte range is still a prefix of HEAD:

| file | base bytes | base `L_N` blank survives at HEAD? | full base prefix in HEAD |
|---|---|---|---|
| `SCORECARD.md` | 206809 (1660 newlines) | yes — HEAD `L1660` `len=0` | yes |
| `LOG.md` | 168871 (1806 newlines) | yes — HEAD `L1806` `len=0` | yes |
| `corpus/SOURCES.md` | 100390 (144 newlines) | yes — base blank is HEAD `L146`; 3 lines inserted before it (`numstat 3 0`) | no (insertion, not loss) |

So defect 6 is not a family symptom: `SCORECARD.md`/`LOG.md` restores in the same `0a24364d` kept the blank; only the SHONEN restore path dropped it.

## 3. Append-only remedy — measured, and it changes the diff shape to `8 0`

Extracted bytes into scratch, appended exactly one `0x0a`:

```
base.md 30157 B / 285 newlines / 34 blanks / 0a0a
tip.md  34691 B / 292 newlines / 33 blanks / 2e0a
fixed.md 34692 B / 293 newlines / 34 blanks / 0a0a
git diff --no-index --numstat base.md tip.md   → 8  1
git diff --no-index --numstat base.md fixed.md → 8  0
```

The one-byte append restores the base convention (`…[~]`.\n\n`), is strictly additive (no history rewrite, no line removed), and is content-neutral: it adds no `Correction (round 43)` literal (r40 `check_h2`/`h2_scan` counts correction lines only) and no `^## ` section (K16 parses sections/placeholders only) — **by inspection, not by execution** (gates are the parent's).

### Durable predicate for the C1 counter (red-before / green-after)
Line-oriented instruments cannot see this byte: `grep -rn 'tail -c' corpus/instruments/` → **0 hits**, and SHONEN is graded only by K14 (correction literals over `RECORDS=(SCORECARD.md LOG.md SHONEN.md)`), K16 (section/placeholder), K18 (transcript quotes). A byte predicate is therefore required:

```sh
B=30157   # base SHONEN byte count
test "$(git show ab98fac9:SHONEN.md | head -c $((B-1)) | sha256sum | cut -d' ' -f1)" \
   = "$(git show HEAD:SHONEN.md      | head -c $((B-1)) | sha256sum | cut -d' ' -f1)"   # prefix intact
test "$(git show HEAD:SHONEN.md | tail -c 2 | xxd -p)" = 0a0a                            # final empty line present
test "$(git show HEAD:SHONEN.md | grep -c '^$')" -ge 34
```
- **red** at `0a24364d..6631401`: `tail -c 2` = `2e0a`, blanks = 33 (first test passes, second/third fail).
- **green** after a one-byte append: `0a0a`, blanks = 34; `numstat base→tip` becomes `8 0` instead of `8 1`.
- A counter written as "`numstat` deletions == 0" alone would be satisfiable by a degenerate rewrite; the tail-blank + prefix pair is the predicate that cannot be faked by truncation (`9e6800ea` fails the prefix test: 4536 B file).

## 4. Do-nothing discrimination

- `.ufo/waves/round-44/controls/do-nothing.txt:2-7` freezes base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` and states no r44 correction and no r44 counter existed. Confirmed at HEAD `6631401`: `ls corpus/instruments/r44-routed-defects.py` → *No such file or directory*, and `SHONEN.md` still ends `2e0a` / 33 blanks.
- Therefore do-nothing leaves defect 6 **unresolved** → C1's "0 of 8 unresolved" is unreachable by replay. Symmetrically, the do-nothing control cannot *report* defect 6 fixed, so C1's kill-rule ("do-nothing replay reports all 8 fixed") is not triggered by this defect.
- The frozen defect text reproduces exactly: "lost one base byte (final empty line)", "in the `0a24364d` restore-and-reappend", "`git diff --stat ab98fac9 dbd2e106 -- SHONEN.md` → `9 +-`" — all three confirmed byte-for-byte. No defect inflation: the delta is 1 byte, content-neutral, with no box, literal, or section affected.

## 5. Limits

- Read-only; I ran no lane gate, no counter, and no formatter (parent owns post-integration gates). Gate-safety of the one-byte append is an inspection claim, not an executed result.
- `8 0` after the fix was measured with `git diff --no-index` over extracted bytes; the lane's `git diff <base> <tip>` on identical bytes should agree (same algorithm) but was not run against a real post-fix commit — no such commit exists.
- If round 44 appends further SHONEN content, the `numstat` figure will change; only the tail-blank + prefix predicate is append-count invariant.
- Scratch used: `${HYAKU_SCRATCH:-/home/vgpnk/.hyaku/scratch}/kasegi-r44/R44Exec4` (`HYAKU_SCRATCH` was unset in this shell, so the default applied); `base.md`/`tip.md`/`fixed.md` deleted and the directory `rmdir`-ed; `ls` on it now returns *No such file or directory*. No `/tmp` use, no tool installs (nothing needed).
- Evidence is committed-byte only (`git show`/`git rev-parse`/`git diff`/`wc`/`xxd`/`sha256sum`/`awk`); no live source re-open was relevant to this item.

## 6. Concurrent worktree state, measured after the sections above (not my edit)

While this seat measured, siblings/L1 landed draft bytes in the shared worktree. Recorded read-only; I wrote none of them.

**The landed fix is byte-identical to the remedy measured in §3.**

```
wc -c SHONEN.md → 34692 ; wc -l → 293 ; tail -c 2 | xxd -p → 0a0a ; grep -c '^$' → 34
sha256(SHONEN.md) → d3018ab826accba006d2fa9b5d0fa113fb5492b75e58007a16b000cc509beccf
git diff --numstat HEAD -- SHONEN.md → 1  0
git diff --no-index --numstat base.md worktree.md → 8  0
sha256(worktree[1..30156]) → c29eee3c9d00b2ecb8a1fcc9cc8151bc11051c5f20663d4a8c829e6739a43d31  (base prefix intact)
```

So the §3 prediction (one `0x0a`, `8 0`, prefix preserved) is confirmed against the actual landed bytes, not only my constructed copy. Committed HEAD is still `6631401` with blob `f7c5072` (tail `2e0a`); the fix is worktree-only at the time of writing.

**Draft counter `corpus/instruments/r44-routed-defects.py` (untracked, 90 lines) — RD43-6 predicate, read not run.**

`:53  ("RD43-6 SHONEN trailing blank line", (root / "SHONEN.md").read_bytes().endswith(b"\n\n"))`

- **Correct half:** this is the durable tail predicate; it is red at the frozen baseline (`5ab3a60` and `6631401` both `f7c5072`, tail `2e0a`) and green on the landed bytes, so a do-nothing replay against the frozen baseline export scores RD43-6 `resolved=0`. The baseline is used only for the frozen defect list (`:74-80` re-derives `expected=8` from `^[1-8]\. \*\*`), never to pin the predicate's input.
- **Gap 1 — the predicate is not base-pinned.** `endswith(b"\n\n")` is also true of the *pre-round* base bytes `ab98fac9` (tail `0a0a`), i.e. of a tree where the defect never existed; and it is true of a truncated `SHONEN.md` that merely ends in a blank line (`9e6800ea`'s 4536 B body would pass if it ended `\n\n`). It proves "ends with a blank line", not "the base's 30157th byte is back". The discriminating form is the pair measured in §3: tail-blank **and** `sha256(file[1..30156]) == c29eee3c…`. Without the prefix half, a degenerate one-byte append to a truncated record scores as fixed.
- **Gap 2 — RD43-6 is the only check reading bytes with an unguarded call.** `:53` calls `.read_bytes()` outside the `text()`/`report_text()` try-except that every other check uses (`:11-26`), so a missing `SHONEN.md` raises `OSError` and aborts the whole counter instead of scoring that one check unresolved. Fail-closed in exit status, but it suppresses the other seven rows' output.

No verdict is claimed on C1/C2 here: the eight-row outcome depends on the other seven predicates and on a run I did not execute (parent owns gates).
