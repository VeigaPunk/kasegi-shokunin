# ScribeProvince receipt — round 31, PROVINCE.md Frontier amendment (F12-F15)

- Seat: `ScribeProvince` (leaf; no subagent dispatched, no swarm). No job was spawned by me; the
  single dependency poll below was auto-backgrounded by the shell tool as `bg_17157` and delivered
  its own result (`iters=27`), which is disclosed rather than described as a foreground run.
- Answering model: `devin/deepseek-v4-1-flash` (route-table default; no model passed).
- Write scope exercised: `PROVINCE.md` (append-only) + this receipt. Nothing else written.
  Scratch lived in `mktemp -d` under `/tmp` and was deleted (`/tmp/tmp.rVjQV3gcYr`).
- No git/jj mutation of any kind: only read-only `git log`, `git show`, `git diff`, `git status`.
- No tool installed or upgraded; no pacman transaction; no network fetch; no live bounty target contacted.

## 1. Pre-state (measured before the edit)

```
$ sha256sum PROVINCE.md
98f7a9dcf9d13e93baf05629fd2033406fb4118827deb01af8a28aa8d2d92304  PROVINCE.md
$ wc -lc PROVINCE.md
  52 2587 PROVINCE.md
$ for t in F12 F13 F14 F15; do printf "%s: " "$t"; grep -c "$t" PROVINCE.md; done
F12: 0
F13: 0
F14: 0
F15: 0
```

So all four admissions were absent, exactly as the seat item states ("verify which of F12, F13,
F14 are absent with grep" — all three were absent, and F15 too).

## 2. Dependency wait (bound 9: poll, no busy-loop)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && F=.ufo/waves/round-31/wave1/ExecEntryF15.md; \
  i=0; until [ -s "$F" ] || [ $i -ge 88 ]; do sleep 20; i=$((i+1)); done; echo "iters=$i"; ls -la "$F"
→ iters=27
→ -rw-r--r-- 1 vgpnk vgpnk 12956 Oct 25 20:39 .ufo/waves/round-31/wave1/ExecEntryF15.md
```

Receipt landed (27 × 20 s ≈ 540 s wait, under the 30-minute cap). No `BLOCKED:` line is needed.

Facts taken from it (read, not retyped from the item): entry `corpus/knowledge/vendor-third-party-
finding-coordination.md`; at the moment I read it through that receipt it was 146 lines, 10359 B,
sha256 `bf40fd9e56351b3a857f5efc45c508889bde75b736915b5c3011c63d36eafa79`;
`source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048` printed
eight `S048:Q1..Q8 OK occurrences=1` lines with `recheck_exit=0`; Q1-Q10 all `pass` (receipt §3).

**In-flight revision (bound 6, disclosed).** Seat `ExecEntryF15` then revised the entry and
reported the final bytes by IRC; re-measured here after the revision:

```
$ sha256sum corpus/knowledge/vendor-third-party-finding-coordination.md
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md
$ wc -lc corpus/knowledge/vendor-third-party-finding-coordination.md
 160 11501 corpus/knowledge/vendor-third-party-finding-coordination.md
$ grep -n "^ground: F15\|^source: S048" corpus/knowledge/vendor-third-party-finding-coordination.md
2:source: S048 — https://www.microsoft.com/en-us/msrc/msvr — section "Microsoft Security Vulnerability Research (MSVR)", capture corpus/source-snapshots/round-31/S048.txt:28-35 — …
5:ground: F15 — a vendor's research programme as an intake route for other vendors' bugs
```

The revision did not touch the header lines my appended text rests on (`:2` `source: S048`, `:5`
`ground: F15`), and the appended PROVINCE line cites only the entry path, its `ground:`/`source:`
header fields and the capture path — no digest and no line count — so it holds on both states. The
146-line digest above is reported as the state that was current when the gate was read, not as the
final bytes.

## 3. Facts each appended statement rests on (re-opened, not remembered)

| Appended statement | Bytes it was read from | Measured this seat |
|---|---|---|
| Frontier section names F01-F10 and F11 only | `PROVINCE.md:37-41` (read raw) + grep counts above | yes |
| `"10/10 admitted"` is the round-25 state, F10 being the round-25 admission | `PROVINCE.md:40` → `corpus objects; 10/10 admitted).`; `PROVINCE.md:39` names `F10, round 25` | yes |
| F12 = Japanese state-coordinated disclosure workflow, round 28 | `corpus/README.md:213` (`| F12 | Japanese state-coordinated disclosure workflow | admitted | …`), corroborated by `corpus/lessons/round-28.md:35` (`frontier admitted 11 → 12`, `PASS F12`) and the r30 amendment `corpus/README.md:288-290` (`F12 at round 28`) | yes |
| F13 = Program severity ladders and reward scales, round 29 | `corpus/README.md:264`; `corpus/lessons/round-29.md:33` (`frontier admitted 12 → 13`, `PASS F13`) | yes |
| F14 = Japanese severity vocabulary and the handling-priority model, round 30 | `corpus/README.md:284`; `corpus/lessons/round-30.md:14` (`Frontier 13 → 14`) | yes |
| F15 admitted round 31, entry `ground: F15`, `source: S048`, capture `corpus/source-snapshots/round-31/S048.txt` | entry header `corpus/knowledge/vendor-third-party-finding-coordination.md:1-5` (read verbatim: `source: S048 — https://www.microsoft.com/en-us/msrc/msvr — …`, `verified-at: 2026-10-25`, `ground: F15 — a vendor's research programme as an intake route for other vendors' bugs`); round-31 `claims.json` C2 (`frontier admitted rows increment 14 -> 15 (F15)`); capture present (`S048.txt` 3755 B); re-verified on the revised final bytes (`:2`, `:5`, sha256 `1f16e371…`, 160 lines) | yes |

Titles/rounds were copied from those rows, not retyped from the seat item.

### Disclosed state at write time (PRE-STATE, non-comparative per bound 6)

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print "frontier=" n+0}' corpus/README.md
frontier=14
$ grep -n "F15" corpus/README.md | head
(no output)
$ grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md
0
```

The `corpus/README.md` F15 row (seat `ScribeReadmeF15`) and the `S048` registry row (seat
`ExecRegistryAppend`) had not landed when I wrote, so the appended text deliberately cites **the
entry's own header and the round-31 claims**, never a README admitted count: the sentence "the
frontier as of round 31 is F01–F15" rests on C2's admission plus the entry's `ground: F15`, not on
`README.md`. Once those rows land, `frontier=15` becomes measurable in README; that is a
main-agent re-run, not a claim of this seat.

## 4. Placement decision (R6)

`corpus/QUALITY.md:40` R6 — "An edit to a file that other files cite by line number keeps every
existing line at its number (append at the end, or a same-line suffix)". Peer `ConnOwnership-2`
(IRC, mid-work) reported that `PROVINCE.md:45-50` and `:52` are cited by line number across the
lane and wave-1 receipts (e.g. `ConnSibling.md:180,183`) and asked for an end-of-file append rather
than an in-Frontier insertion. I acknowledged and complied: the block starts at line 53 and the
Frontier paragraph is untouched.

Existing in-lane citations to PROVINCE.md lines, enumerated (all ≤ 52, all unchanged):

```
$ grep -rn "PROVINCE\.md:[0-9]" --include="*.md" .ufo/waves/round-31 .ufo/waves/round-30 \
    | grep -o "PROVINCE\.md:[0-9-]*" | sort | uniq -c | sort -rn
      4 PROVINCE.md:3
      3 PROVINCE.md:52
      3 PROVINCE.md:45-50
      1 PROVINCE.md:38
      1 PROVINCE.md:31-40
      … (plus out-of-range/foreign citations such as :3-300, :283-287, :3-193 — these were already
      out of range at base and are not touched or fixed by this seat)
```

R6 proof — the cited lines are byte-identical:

```
$ diff <(git show HEAD:PROVINCE.md | sed -n '45,50p;52p') <(sed -n '45,50p;52p' PROVINCE.md) \
    && echo R6_ANCHORS_IDENTICAL
R6_ANCHORS_IDENTICAL
```

Anchor instrument, before (HEAD bytes in a temp dir) vs after (worktree) — identical:

```
$ python3 corpus/instruments/anchorcheck.py PROVINCE.md      # BEFORE, on HEAD copy in /tmp
== PROVINCE.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
$ python3 corpus/instruments/anchorcheck.py PROVINCE.md      # AFTER, worktree
== PROVINCE.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
anchorcheck_exit=0
```

(`PROVINCE.md` cites only paths, never `path:line`, so the instrument reports 0 cite instances both
before and after; the line-stability evidence is the `diff` above and the zero-deletion diff below.)

## 5. Additions-only proof

```
$ git diff --stat -- PROVINCE.md
 PROVINCE.md | 20 ++++++++++++++++++++
 1 file changed, 20 insertions(+)
$ git diff --numstat -- PROVINCE.md
20	0	PROVINCE.md
$ git diff -U0 -- PROVINCE.md | grep -c '^-[^-]'
0
$ sha256sum PROVINCE.md ; wc -lc PROVINCE.md
b42e5fbbbcdd7332ea971d8f9f0500965cc22f485e7766536c488a7e31a96076  PROVINCE.md
  72 4007 PROVINCE.md
```

Full unified diff (`git diff --no-color -U3 -- PROVINCE.md`, written to a temp file and read back
because the shell renderer elides diff bodies):

```diff
diff --git i/PROVINCE.md w/PROVINCE.md
index abace49..adf7015 100644
--- i/PROVINCE.md
+++ w/PROVINCE.md
@@ -50,3 +50,23 @@ Sibling lanes are reported, not absorbed:
 - kengaku — LLM evaluation and benchmarks
 
 Live-target testing is refused; this corpus is documentation only.
+
+## Frontier amendment — F12-F15 (appended round 31, 2026-10-25)
+
+[r31 amendment, appended 2026-10-25; end-of-file append per R6, so every existing line keeps its
+number] The Frontier section above names F01–F10 and F11 only. This amendment appends the four
+admissions it does not name, without editing that paragraph:
+
+- F12 — Japanese state-coordinated disclosure workflow — admitted round 28
+- F13 — Program severity ladders and reward scales — admitted round 29
+- F14 — Japanese severity vocabulary and the handling-priority model — admitted round 30
+- F15 — vendor-side research programme as an intake route for other vendors' bugs (Microsoft
+  MSVR) — admitted round 31; entry `corpus/knowledge/vendor-third-party-finding-coordination.md`
+  (header `ground: F15`, `source: S048`, capture `corpus/source-snapshots/round-31/S048.txt`)
+
+[r31 correction, R9] The "10/10 admitted" parenthetical in the Frontier paragraph above is the
+round-25 frontier state (F10 was the round-25 admission) and is retained as history rather than
+rewritten; the frontier as of round 31 is F01–F15. Titles and round attributions for F12–F14 are
+read from the `corpus/README.md` frontier rows at :213, :264 and :284; F15's round attribution is
+this round's admission (round-31 claims, C2), and its entry binds the frontier as `ground: F15`
+against the round-31 capture `corpus/source-snapshots/round-31/S048.txt`.
```

Line map of the appended block (worktree): `:53` blank, `:54` `## Frontier amendment — F12-F15 …`,
`:56-58` R6/scope note, `:60-65` the four admission bullets (F15 spans `:63-65`), `:67-72` the R9
correction line. Verified with `awk 'NR>=52 && NR<=72 {printf "%d|%s\n", NR, $0}' PROVINCE.md`.

## 6. Post-state grep

```
$ for t in F12 F13 F14 F15; do printf "%s=%s " "$t" "$(grep -c "$t" PROVINCE.md)"; done
F12=3 F13=1 F14=2 F15=6
```

(F12 appears in the heading, its bullet and the `F12–F14` provenance clause; F15 in the heading,
bullet and capture sentence twice, etc. — counts are raw `grep -c` occurrences, not distinct lines.)

## 7. Findings and limits

1. **R9 honoured by appending, not rewriting.** `PROVINCE.md:37-40` (the `F01–F10 … 10/10 admitted`
   paragraph) is byte-identical; the correction is the appended `[r31 correction, R9]` line at
   `:67-72`.
2. **No count is retyped.** Every round attribution comes from a re-opened README row or lesson
   line, and F15's from the landed entry header plus C2 — each named in §3.
3. **Limit (disclosed, not worked around):** the README F15 row and the S048 registry row were
   still absent at write time (§3). This receipt therefore asserts nothing about README's admitted
   count; `frontier=15` is the main agent's re-run once `ScribeReadmeF15` and `ExecRegistryAppend`
   land. Likewise the `frontier-recheck-count.py` harness is PRE-STATE for F15 and is not cited here.
4. **Out of scope, untouched:** `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*`,
   `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `SKILL.md`, the report, `claims.json`, and the
   campaign package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (never written, its tools never run).
5. **Checks the main agent should run once the wave is quiescent:** `git diff -- PROVINCE.md` at the
   integration commit (expect additions only, 20 lines, zero deletions), `grep -c 'F1[2-5]'
   PROVINCE.md`, the R6 anchor `diff` in §4, and — after `ScribeReadmeF15` lands — the README
   admitted-row count (`awk` in §3) to confirm `frontier=15` matches the appended sentence.
