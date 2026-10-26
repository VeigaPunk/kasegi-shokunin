# ScribeProvince receipt — round 33, PROVINCE.md Frontier amendment (F16)

- Seat: `ScribeProvince` (leaf; no subagent, no swarm, no labrat). No job was spawned by me; the
  four background jobs below were auto-backgrounded by the shell tool while the shared session
  shell was busy, and are disclosed rather than described as foreground runs.
- Answering model: `opencode-go/deepseek-v4.1-flash` (config route table; no model passed by hand —
  the same runtime line `ExecEntryF16.md` records). Tools installed/upgraded: none; no pacman
  transaction (host pause), no network fetch, no live bounty target contacted, no git/jj mutation.
- Write scope exercised: `PROVINCE.md` (append-only, lane-relative) + this receipt. Nothing else.
- Scratch: `$HYAKU_SCRATCH/kasegi-r33/ScribeProvince/` (one HEAD copy of `PROVINCE.md` for the
  before-anchorcheck). Removed and verified gone; the first shell's `trap` did not fire under the
  temporary-shell wrapper, so removal was redone explicitly (§5).

## 1. Pre-state (measured before the edit)

```
$ git rev-parse HEAD ; git log --oneline -1
a6a502351bb90c8cd6d9b8f45f55109b7848e0d1
a6a5023 round-33: wave-1 spec (64 seats, v2 policy), validated plan and dispatch
$ wc -l PROVINCE.md ; sha256sum PROVINCE.md
72 PROVINCE.md
b42e5fbbbcdd7332ea971d8f9f0500965cc22f485e7766536c488a7e31a96076  PROVINCE.md
$ git status --porcelain PROVINCE.md
(no output — clean)
$ grep -c F16 PROVINCE.md
0
```

F16 was absent from PROVINCE.md before the edit (item requirement: verify with grep).

## 2. Dependency wait (bound 9: poll, no busy-loop)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && F=.ufo/waves/round-33/wave1/ExecEntryF16.md; \
    i=0; until [ -s "$F" ] || [ $i -ge 88 ]; do sleep 20; i=$((i+1)); done; echo "iters=$i"; ls -la "$F"
iters=30
-rw-r--r-- 1 vgpnk vgpnk 16732 Oct 26 01:26 .ufo/waves/round-33/wave1/ExecEntryF16.md
```

Landed after 30 × 20 s ≈ 601 s (under the 30-minute cap; tool auto-backgrounded it as `bg_281`; a
short second poll was auto-backgrounded as `bg_555` and also saw the file). No `BLOCKED:` line is
needed. I read the receipt in full and did not edit any peer file.

Facts taken from it (read, not retyped from the item): entry
`corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`, Q1–Q10 self-check all pass,
header `ground: F16`, both `source:` ids, and `frontier-recheck-count.py` on the lane tree
PRE-STATE 18/18 with `PASS F16 ids=S049,S050` shown only on a scratch copy carrying the not-yet-
landed README row.

## 3. Entry bytes at write time (re-measured, M30-3 disclosed)

The entry was still being revised while I waited. Two states were measured; the appended PROVINCE
line cites neither digest nor line count, so it holds on both:

```
$ sha256sum corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md   # 01:23, mid-flight
8d209995ec5af1129fab2238cb92dbba2fd68700dbeabd5c05d921f50669d08c
$ wc -lc ...                                                                     # 01:23
  278 21970 corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md

$ sha256sum corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md   # 01:25, final
eebd5ea572b3359f012e9c7ef9975969ffcbd3e5b06e31d40ac56a6a7d15910b
$ wc -lc ...                                                                     # 01:25
  305 24318 corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
$ grep -n "^ground:\|^source: S04\|^source: S050\|^verified-at:" ... | cut -c1-80
3:source: S049 — https://zc.cnvd.org.cn/news/helpList — 网络安全众测…
4:source: S050 — https://security.360.cn/Reward/rules — 360SRC 外部漏洞…
5:verified-at: 2026-10-26
6:ground: F16
```

The final state matches `ExecEntryF16.md` §1 (`eebd5ea5…`, 305 lines, 24318 B). Registry rows had
also landed (`corpus/SOURCES.md:55-56` carry `S049`/`S050`); the README F16 row had not
(`corpus/README.md` F16 count 0 at write time), so the appended text asserts nothing about the
README admitted count.

## 4. Placement decision (R6)

`corpus/QUALITY.md:40` R6 — "An edit to a file that other files cite by line number keeps every
existing line at its number (append at the end, or a same-line suffix)". In-lane citations of
`PROVINCE.md` lines, enumerated over the lane's wave receipts/lessons:

```
$ grep -rno "PROVINCE\.md:[0-9][0-9-]*" --include="*.md" .ufo/waves/round-3* \
    | sed 's/.*PROVINCE/PROVINCE/' | sort | uniq -c | sort -rn | head -8
      5 PROVINCE.md:45-50
      4 PROVINCE.md:52
      2 PROVINCE.md:3
      1 PROVINCE.md:7-13
      1 PROVINCE.md:45-70
      1 PROVINCE.md:43-52
      1 PROVINCE.md:40
      1 PROVINCE.md:37-41
```

Peer `ConnOwnership` (IRC, mid-work) independently flagged `:3, :16-22, :29, :31-40, :37, :38`
(including `corpus/lessons/round-24-verifier-spotcheck.md:112` on `:38`) and allowed either an
insertion at the end of the `## Frontier` section (after the F15 row) or an EOF append into the
`Frontier amendment` block. I chose the EOF append: the file is owned append-only, and it keeps all
32 existing lines byte-identical, including every cited one. I replied to `ConnOwnership` with the
placement and the proof below.

R6 proof — every cited line is byte-identical:

```
$ diff <(git show HEAD:PROVINCE.md | sed -n '3p;7,13p;37,52p') <(sed -n '3p;7,13p;37,52p' PROVINCE.md) \
    && echo R6_ANCHORS_IDENTICAL
R6_ANCHORS_IDENTICAL
$ diff <(git show HEAD:PROVINCE.md | sed -n '1,72p') <(sed -n '1,72p' PROVINCE.md) \
    && echo FIRST_72_LINES_IDENTICAL
FIRST_72_LINES_IDENTICAL
```

Anchor instrument, before (HEAD copy) vs after (worktree) — identical (PROVINCE.md cites paths,
never `path:line`, so the instrument reports 0 cite instances in both states):

```
$ python3 corpus/instruments/anchorcheck.py PROVINCE.md      # BEFORE, HEAD copy under $HYAKU_SCRATCH
== PROVINCE.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
before_exit=0
$ python3 corpus/instruments/anchorcheck.py PROVINCE.md      # AFTER, worktree
== PROVINCE.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
anchorcheck_exit=0
```

## 5. The append and additions-only proof

Appended text (one factual line plus the blank separator, at EOF, `:73-74`):

```
[r33 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F16 — Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC) — admitted round 33
```

The quoted admission text is reproduced exactly; byte check of `:74` shows the UTF-8 em dash
(`e2 80 94`) and `众测` (`e4 bc 97 e6 b5 8b`), line terminated by `0a`.

```
$ git diff --stat -- PROVINCE.md
 PROVINCE.md | 2 ++
 1 file changed, 2 insertions(+)
$ git diff --numstat -- PROVINCE.md
2	0	PROVINCE.md
$ git diff -U0 -- PROVINCE.md | grep -c '^-[^-]'
0
```

Full unified diff:

```diff
diff --git i/PROVINCE.md w/PROVINCE.md
index adf7015..791ae06 100644
--- i/PROVINCE.md
+++ w/PROVINCE.md
@@ -70,3 +70,5 @@ rewritten; the frontier as of round 31 is F01–F15. Titles and round attributio
 read from the `corpus/README.md` frontier rows at :213, :264 and :284; F15's round attribution is
 this round's admission (round-31 claims, C2), and its entry binds the frontier as `ground: F15`
 against the round-31 capture `corpus/source-snapshots/round-31/S048.txt`.
+
+[r33 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F16 — Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC) — admitted round 33
```

Scratch cleanup (the `trap` did not fire inside the temporary-shell wrapper; redone explicitly):

```
$ ls -la /fast/scratch/hyaku/kasegi-r33/ScribeProvince      # after the trap attempt
-rw-r--r-- 1 vgpnk vgpnk 4007 Oct 26 01:27 PROVINCE.md
$ rm -rf -- /fast/scratch/hyaku/kasegi-r33/ScribeProvince
$ ls -d /fast/scratch/hyaku/kasegi-r33/ScribeProvince
ls: cannot access '/fast/scratch/hyaku/kasegi-r33/ScribeProvince': No such file or directory
```

## 6. Post-state

```
$ wc -lc PROVINCE.md ; sha256sum PROVINCE.md
  74 4194 PROVINCE.md
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  PROVINCE.md
$ grep -c F16 PROVINCE.md
1
$ grep -c -F 'F16 — Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC) — admitted round 33' PROVINCE.md
1
$ git status --porcelain PROVINCE.md
 M PROVINCE.md
```

## 7. Facts the appended line rests on

| Appended statement | Re-opened evidence | Measured this seat |
|---|---|---|
| F16 title "Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC)" | `ExecEntryF16.md` §2 header (`ground: F16`, `source: S049`/`source: S050`); entry `:1` H1, `:3-4`, `:6`; round-33 `claims.json` C2 surface ("Frontier F16 'Chinese crowdsourced-testing platform scope and reward rules'") | yes |
| "admitted round 33" | round-33 `claims.json` C2 (frozen predicate: frontier admitted rows 15 → 16 (F16)) plus the entry landing in this round; the C2 harness number on the real tree is the parent's re-run (README row not yet landed) | yes, as C2's frozen target — no README count asserted |

No number is retyped from the item: the title string comes from the entry header/claims surface, the
round from the round-33 frozen claim, and the line text from the seat item's quoted string.

## 8. Findings and limits

1. **Append-only honoured.** `PROVINCE.md:1-72` is byte-identical to HEAD; the only change is the
   blank line + one factual line at `:73-74`. No existing paragraph was rewritten (R9 history stays;
   the r31 amendment block is untouched).
2. **Placement is R6-safe.** All 15 previously cited `PROVINCE.md:<line>` anchors are unaffected;
   the peer flag (`ConnOwnership`) named the same constraint and I complied with the EOF option.
3. **Limit (disclosed):** at write time `corpus/README.md` had no `| F16 |` row (ScribeReadmeF16's
   file) and the lane harness read `entries=18 pass=18` (PRE-STATE for F16). The appended line
   therefore does not cite the README admitted count and the harness is not cited as an after state.
   The `entries=19 pass=19` / `PASS F16 ids=S049,S050` figure in `ExecEntryF16.md` §5 is a
   fixture-tree number on a copied README, not the lane's gate.
4. **Mid-flight bytes disclosed (M30-3):** the entry was measured at `8d209995…` (278 lines) and at
   its final `eebd5ea5…` (305 lines); only the final state's header lines were used.
5. **Out of scope, untouched:** `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*`,
   `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `SKILL.md`, `corpus/instruments/*`, `claims.json`,
   `c1-controls/`, `c2-controls/`, `assimilation/`, the report, and `/home/vgpnk/Projects/shokuknow`
   (read-only; its campaign tools never run).
6. **Checks the main agent should run once the wave is quiescent:** `git diff -- PROVINCE.md` at the
   integration commit (expect 2 insertions, 0 deletions), `grep -c F16 PROVINCE.md` → 1, the R6
   `diff` in §4, and — after `ScribeReadmeF16` lands — `frontier-recheck-count.py` on the real tree
   (expect `entries=19 pass=19` incl. `PASS F16 ids=S049,S050`) and the README admitted-row `awk`
   (expect 16).
