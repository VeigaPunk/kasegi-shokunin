# ExecLessonErrata — round-34 wave 1 receipt

Seat: executor (`ExecLessonErrata`), round 34, lane `kasegi-shokunin` (base `014ee2d`,
claims-freeze `29f606db`). Answering model: `opencode-go/deepseek-v4.1-flash` (harness project
context; not passed to this seat). Tools installed/upgraded: none.

Subject: append R7 + M33-3 errata (assignment) and, because `ExecRDefectClosureSuite`'s R4 closure
check requires it and no seat is assigned it, the R4 erratum in the same file. All three blocks
are append-only; no existing line was edited (`head -138` / `head -263` byte-identical, numstat
0 deletions).

## Report

### 0. Files changed (2) — production, lane repo

| File | Before (HEAD `206e510`) | After | Delta |
|---|---|---|---|
| `corpus/lessons/round-33.md` | `ca17591d4a36e1a6623adb9acb7ac2bc0a3dbd87c24f3913229fe0b4b781feb2`, 138 lines | `f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807`, 247 lines | `+109 −0` (`git diff --numstat`: `109 0`) |
| `corpus/lessons/round-29.md` | `78ae8080fc3653b2f7291df7fd229ff4aeccc9965db2042c1825ca1f5aa52f5b`, 263 lines | `4afb96be18355cd958f9ddccc4f9687c2c2afa4b2747d49f687add956484ecce`, 337 lines | `+74 −0` (`git diff --numstat`: `74 0`) |

Append-only proof (run 2026-10-26T05:39Z):

```
$ head -138 corpus/lessons/round-33.md | sha256sum
ca17591d4a36e1a6623adb9acb7ac2bc0a3dbd87c24f3913229fe0b4b781feb2  -     # == pre-append file
$ head -263 corpus/lessons/round-29.md | sha256sum
78ae8080fc3653b2f7291df7fd229ff4aeccc9965db2042c1825ca1f5aa52f5b  -     # == pre-append file
$ git diff corpus/lessons/round-33.md corpus/lessons/round-29.md | grep -c '^-[^-]'
0
$ git diff corpus/lessons/round-33.md corpus/lessons/round-29.md | grep -c 'LANE_HASH'
0
```

New section headings:

```
corpus/lessons/round-33.md:140:## Erratum (round 34) — R7: the S049/S050 quote counts and the S050 sentence line
corpus/lessons/round-33.md:215:## Erratum (round 34) — R4: "all mutants killed" overstated; the frozen kill rule caught 3 of 4
corpus/lessons/round-29.md:265:## Erratum (round 34) — M33-3: the `SOURCES.md` line anchors cited from this lesson are stale by +7
```

### 1. R7(a) — the two quote counts, measured

Filed at `corpus/lessons/round-33.md:31-32` as "19 characters" (S049) and "23 characters" (S050).
Producing command (2026-10-26T05:32Z):

```
$ printf '%s' '众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。' | wc -m
31
$ printf '%s' '未纳入安全服务的资产一般情况下不收录相关漏洞' | wc -m
22
$ printf '%s' '「众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。」' | wc -m
33
$ printf '%s' '「未纳入安全服务的资产一般情况下不收录相关漏洞」' | wc -m
24
```

So 19 → **31** and 23 → **22**; the 「」 delimiters are excluded (33/24 with them), which the block
declares so the number re-derives. Occurrence binding on the committed captures:

```
$ grep -cF '众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。' corpus/source-snapshots/round-32/S049.txt
1
$ grep -cF '未纳入安全服务的资产一般情况下不收录相关漏洞' corpus/source-snapshots/round-32/S050.txt
1
```

Independent agreement: `.ufo/waves/round-33/wave1/RevGateSpot.md` § Findings 1 (`len()` → 31 and 22).
Quotes, locations (`S049.txt:214`, `S050.txt:591`), access dates and digests stand; both admits stand.

### 2. R7(b) — the S050 applicability sentence is at L70, heading at L69

```
$ awk 'NR>=69 && NR<=71 {printf "%d: %s\n", NR, $0}' corpus/source-snapshots/round-32/S050.txt
69: 一、适用范围
70: 本标准适用于 360 集团发布的产品和业务，此外 360 集团所投资的公司、子公司、合资公
71: 司等也在收录范围内，具体范围可参考 https://security.360.cn/Product/product。
$ grep -nF '本标准适用于 360 集团发布的产品和业务' corpus/source-snapshots/round-32/S050.txt | cut -c1-40
70:本标准适用于 360 集团发布的产品和业务，
$ grep -cF '一、适用范围' corpus/source-snapshots/round-32/S050.txt
2        # L25 table-of-contents copy + L69 heading
```

The one sentence-level `:69` citation is the fleet report:

```
$ sed -n '61p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md   (cut)
**Gate** … F16/S050 with 「本标准适用于 360 集团发布的产品和业务」 (S050.txt:69) and …
$ sha256sum /home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md
0a2c6758705df4bf28b018b0a1c00974f528d7811951ec3fa3333e3c41b3e7c6
```

Corrected to `S050.txt:70` in the appended block (the fleet report is outside the lane's write
scope and was only read). Every other pointer was classified in the block; the lane sweep found no
production file citing `:69` for the sentence:

```
$ grep -rn 'S050\.txt:69\|(L69\|适用范围 L69' --include=*.md corpus/ SCORECARD.md LOG.md SKILL.md
corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:4   # section span 一、适用范围 (L69-71)
corpus/lessons/round-33-verifier-spotcheck.md:181                      # the R7 routing text itself
corpus/SOURCES.md:56                                                   # row cell: L69-71, "sentence wraps across L70-L71"
corpus/SOURCES.md:99                                                   # registry-changes line
$ echo $?
0
```

Entry `:97` already cites `S050.txt:70`; `round-32-verifier-spotcheck.md:73` ("适用范围 at L69") names
the heading; `round-33.md:46` cites the section `§一 L69–71`. All correct as filed.

### 3. R4 — "all mutants killed" overstated (added beyond the literal assignment)

Fleet report verdict line: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md:49` =
"C1: target met. 40/40/0 with all mutants killed, fake rejected, selftest 11/11".

Measured facts quoted by the appended block (both from round-33 receipts, read at tip):
`wave1/RevClaimsFreeze.md` § "The four counter mutants" — M1/M2/M3 caught (`failures=1` each);
M4 skip-selftest prints `selftest cases=9 failures=0` exit 0 without running a fixture, **not**
caught by the kill-rule text (finding F-5: "M4 skip-selftest is **NOT** caught by the kill rule
text"); `wave1/MutCtrUnbound.md` § Verdict — "**SURVIVOR** under the frozen C1 kill rule as tasked
(plain run)", `records=2 bound=2 unbound=0` exit 0 on a url-less fixture, both pinned generations.
The block states "3 of 4 (3/4)" and names both survivors and the outside-the-plain-run clauses that
kill them. Greppable anchors on disk:

```
$ grep -c "all mutants killed" corpus/lessons/round-33.md      -> 3
$ grep -c "3 of 4"            corpus/lessons/round-33.md      -> 2
$ grep -c "RevClaimsFreeze.md" corpus/lessons/round-33.md     -> 2
$ grep -c "MutCtrUnbound.md"   corpus/lessons/round-33.md     -> 4
```

Why it is here: `ExecRDefectClosureSuite`'s R4 check requires "the round-33 lesson carries an
appended erratum correcting the 'all mutants killed' overstatement to the measured
3-of-4-under-frozen-rule figure"; no wave-1 seat's assignment names that append, and this seat is
the sole writer of `corpus/lessons/round-33.md`. L1: acknowledge or strike this block — C1's R4
limb depends on it. Messaged `ExecRDefectClosureSuite` with the exact literals.

### 4. M33-3 — `SOURCES.md` anchor drift, re-opened against the cited revisions

```
$ for rev in 0ab8929 690b69d 9f98488 HEAD; do
>   printf '%s lines=%s ' "$rev" "$(git show $rev:corpus/SOURCES.md | wc -l)"
>   git show $rev:corpus/SOURCES.md | grep -n '^## \|^Change cell old → new: the S043' | cut -d: -f1 | tr '\n' ' '
>   echo
> done
0ab8929 lines=86 3 53 60 70 76 83
690b69d lines=94 3 56 63 74 80 87
9f98488 lines=100 3 58 65 77 83 90
HEAD lines=100 3 58 65 77 83 90
```

Column order = `## Registry` · `## Paths` · `## Search log` · `## Leads (unopened)` · `## Registry
changes` · S043 R8 change cell. So the two round-29-era pointers to `corpus/SOURCES.md:83`
(`corpus/lessons/round-29.md:214` in M29-9; `corpus/lessons/round-29-verifier-spotcheck.md:74`)
now resolve to **`:90`** (+7); `:83` is the `## Registry changes` heading. `M29-9`'s "row cell
(line 49)" is still line 49 (`grep -n '^| S043 ' corpus/SOURCES.md` → 49). Today's file:
100 lines, sha256 `b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b` — same at
`014ee2d` and `HEAD`. The spotcheck pointer is named in the erratum and left byte-identical (not
this seat's assigned path).

### 5. Final state checks

```
$ sha256sum corpus/lessons/round-33.md corpus/lessons/round-29.md
f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807  corpus/lessons/round-33.md
4afb96be18355cd958f9ddccc4f9687c2c2afa4b2747d49f687add956484ecce  corpus/lessons/round-29.md
$ wc -l corpus/lessons/round-33.md corpus/lessons/round-29.md
247 corpus/lessons/round-33.md
337 corpus/lessons/round-29.md
$ git status --porcelain corpus/lessons/
 M corpus/lessons/round-29.md
 M corpus/lessons/round-33.md
```

Digest history of this seat's round-33 append: `8d6331fc…06dbcbf` (first write, 246 lines) →
`f69472f3…f388807` (247 lines) after one amendment inside the new R4 block: the sentence naming
`corpus/instruments/kill-rule-check.py` was rewritten to carry the R1 facts (`test -e` → exit 1 at
2026-10-26T05:42Z; landing in this same round) instead of asserting an absent path as live. No
round-33 filed line was touched by that amendment (prefix digest unchanged, `head -138` →
`ca17591d…`).

No git/jj mutation issued by this seat (`log`, `show`, `diff`, `status`, `rev-parse` only). No write
outside the lane; the fleet round-33 report, `/home/vgpnk/Projects/shokuknow` and sibling lanes were
read-only. Scratch `/fast/scratch/hyaku/kasegi-r34/ExecLessonErrata/` (three evidence files) was
removed before this receipt was finalised; `ls /fast/scratch/hyaku/kasegi-r34/ExecLessonErrata` →
No such file or directory.

### Risks / open for the L1

1. **R4 block is beyond this seat's literal assignment** (see §3). It is required by
   `ExecRDefectClosureSuite`'s R4 limb and no other seat owns the file. Keep or strike; C1's
   `closed=9/9` depends on it.
2. **`corpus/lessons/round-29-verifier-spotcheck.md:74` still cites `SOURCES.md:83`.** Not in this
   seat's assigned paths; the round-29 erratum names the correction (`:90`). An owner for that file
   should append the same one-line correction if the lane wants the sweep literally complete.
3. **Fleet report `kasegi.md:61` still prints `(S050.txt:69)`** — read-only to the lane. The
   correction of record is the appended R7 block; if the fleet report is re-edited by its owner,
   the corrected value is `S050.txt:70`.
4. Anchor numbers in §4 move with every future `SOURCES.md` append; the block tells a reader to
   re-measure or cite the anchor text instead of a number.
