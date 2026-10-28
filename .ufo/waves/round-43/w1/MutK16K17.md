# MutK16K17 — one-limb mutation battery for K16 (placeholder promise) and K17 (claims before-literal)

Seat: leaf mutation-tester, kasegi round 43, one v2 wave. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Receipt-only item: this file is the only lane write. Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Scratch `S=/fast/scratch/hyaku/kasegi-r43/MutK16K17` (removed at exit; nothing here depends on it surviving).

## Tested bytes (the mutant substrate)

| object | path | lines | sha256 |
|---|---|---|---|
| K16 limb | `.ufo/waves/round-43/w1/ExecK16Placeholder.sh` | 213 | `d7c33c9efdcfb5ab0feeac494da6a12d83d95d9b0d2d20b2bd121ba7af5a74cb` |
| K17 limb | `.ufo/waves/round-43/w1/ExecK17ClaimsBefore.sh` | 591 | `37a513ed7dfbc8dd83d6a77da2a44843ea424e0a932fb501bea681ccedc7f348` |
| detector K16 (scratch) | `k16_detector.py` | 143 | 11 fixture cases |
| detector K17 (scratch) | `k17_detector.py` | 144 | 10 fixture cases |

Both limbs are uncommitted deliverables at the time of the probe (the instrument `corpus/instruments/r43-closure.sh`
does not exist at base; the limbs are its future K16/K17 bodies). The battery therefore mutates the delivered limb
files, not the suite.

K17 churn observed while probing: delivered bytes were `fe046218…` (13:47) → `c1a123f5…` (13:48) →
`37a513ed…` (13:49). The full battery was re-run on each. The last two revisions differ in the header comment only
(`diff -u` = 16 lines, all `#` text); `grade()` — the mutated surface — is byte-identical in all three.
The verdict table below is against **37a513ed**. The first revision's selftest-driver rewrite (`rewrite` → `subst`)
does not touch `grade()` either.

```
$ sha256sum .../w1/ExecK16Placeholder.sh .../w1/ExecK17ClaimsBefore.sh
d7c33c9efdcfb5ab0feeac494da6a12d83d95d9b0d2d20b2bd121ba7af5a74cb  ExecK16Placeholder.sh
37a513ed7dfbc8dd83d6a77da2a44843ea424e0a932fb501bea681ccedc7f348  ExecK17ClaimsBefore.sh
```

## Method

One behavioral detector per limb, run unchanged over pristine → mutated → restored bytes:

```
$ cp <delivered limb> $S/limbs/k16-pristine.sh        # and k17
$ python3 $S/k16_detector.py $S/limbs/k16-pristine.sh $S/fx/k16
$ cp $S/limbs/k16-pristine.sh $S/mut/k16/M1.sh        # then one `edit` patch per mutant
$ python3 $S/k16_detector.py $S/mut/k16/M1.sh $S/fx/k16
$ cp $S/limbs/k16-pristine.sh $S/work/limb.sh         # restore, cmp, re-run
```

Each mutant is exactly one behavioral limb. Invocation is the limb's sourceable contract:
`bash -c '. "$1"; check_k16 "$2"'` / `. "$1"; check_k17 "$2"`. K17's real committed base export
(`git -C <lane> archive ab98fac9 | tar -x`, 152 MB, under `$S/base`) is a second, independent detector
for every K17 mutant.

Fixture expectations come from the frozen claim text, not from the pristine limb: a detector that only
recorded pristine output could never see a defect. Pristine passes every case (below), so the detector
is sound; any mutant failing a case is killed.

### Pristine baselines (unchanged detector)

```
$ python3 $S/k16_detector.py $S/limbs/k16-pristine.sh $S/fx/k16
case=c1_base_red expected=0 actual=0 rc=1 verdict=pass
case=c2_resolved_green expected=1 actual=1 rc=0 verdict=pass
case=c3_fenced_only_promise expected=1 actual=1 rc=0 verdict=pass
case=c4_fenced_pseudo_heading expected=1 actual=1 rc=0 verdict=pass
case=c5_near_token_tbd expected=1 actual=1 rc=0 verdict=pass
case=c6_correction_wrong_heading expected=0 actual=0 rc=1 verdict=pass
case=c7_correction_other_file expected=0 actual=0 rc=1 verdict=pass
case=c8_no_promise expected=0 actual=0 rc=1 verdict=pass
case=c9_no_sections expected=0 actual=0 rc=1 verdict=pass
case=c10_quoted_promise expected=1 actual=1 rc=0 verdict=pass
case=c11_unreadable expected=notclosed actual=none rc=1 verdict=pass
detector cases=11 failures=0 verdict=PASS
```

```
$ python3 $S/k17_detector.py $S/limbs/k17-pristine.sh $S/fx/k17
case=q1_unbacked_red expected=0 actual=0 rc=1 payload=claims=1,tokens=1,verified=0,superseded=0,unbacked=1 verdict=pass
case=q2_backed_green expected=1 actual=1 rc=0 payload=claims=1,tokens=1,verified=1,superseded=0,unbacked=0 verdict=pass
case=q3_erratum_other_token expected=0 actual=0 rc=1 payload=claims=1,tokens=1,verified=0,superseded=0,unbacked=1 verdict=pass
case=q4_near_token expected=0 actual=0 rc=1 payload=claims=1,tokens=1,verified=0,superseded=0,unbacked=1 verdict=pass
case=q5_other_round_control expected=0 actual=0 rc=1 payload=claims=1,tokens=1,verified=0,superseded=0,unbacked=1 verdict=pass
case=q6_unparseable expected=0 actual=0 rc=1 payload=claims=2,tokens=1,verified=1,superseded=0,unbacked=0,parse=1 verdict=pass
case=q7_quoted_record expected=1 actual=1 rc=0 payload=claims=1,tokens=1,verified=1,superseded=0,unbacked=0,quoted=1 verdict=pass
case=q8_after_target expected=1 actual=1 rc=0 payload=claims=1,tokens=1,verified=1,superseded=0,unbacked=0 verdict=pass
case=q9_no_tokens expected=0 actual=0 rc=1 payload=claims=1,tokens=0,verified=0,superseded=0,unbacked=0 verdict=pass
case=q10_fenced_cell_token expected=0 actual=0 rc=1 payload=claims=1,tokens=1,verified=0,superseded=0,unbacked=1 verdict=pass
detector cases=10 failures=0 verdict=PASS
```

Fixture shapes (built by the detectors):
K16 — c1 r42 lesson promise with no correction; c2 same + appended naming correction; c3 promise vocabulary only in a
fenced block of an unresolved section; c4 `## Fake` heading inside a fence; c5 `TBDX` near token; c6 `Correction (round 43)`
naming a different heading; c7 correction for A's heading parked in LOG.md; c8 sections, no promise; c9 no sections;
c10 promise vocabulary inside backticks; c11 one unreadable scanned file.
K17 — q1 before `closed=10/12` vs cited control printing `closed=8/12`; q2 both `closed=8/12`; q3 erratum carrying
`superseded` that quotes `closed=9/9`, not the token; q4 control prints only `closed=10/120`; q5 the matching value sits
in round-41's control, not the cited round-42 one; q6 valid backed round + an unparseable `claims.json`; q7 cell quotes
`corpus/lessons/round-42.md` "which says closed=10/12" beside the cited receipt's `closed=8/12`; q8 `after` carries
`closed=13/13` that no control prints; q9 no token; q10 token inside a fenced block in the cell.

## K16 — ExecK16Placeholder.sh (sha `d7c33c9e…`, 213 lines)

| # | mutant | patch (pristine → mutant) | killed by | verdict |
|---|---|---|---|---|
| M1 | drop fenced-block exclusion | `if fence is not None:` + `continue` → `if fence is not None and clauses(...): fenced += 1` (lines inside a fence fall through into heading/body handling) | `c3_fenced_only_promise` `c4_fenced_pseudo_heading` | **killed** (2 cases) |
| M2 | drop whole-token boundary | `("tbd", re.compile(r"\bTBD\b"))` → `("tbd", re.compile(r"TBD"))` | `c5_near_token_tbd` | **killed** |
| M3 | accept a supersede line without the token | `if CORRECTION in line and heading in line:` → `if CORRECTION in line:` | `c6_correction_wrong_heading` | **killed** |
| M4 | accept the naming token from outside the file (K16 has no other-round control surface; analogue = the same-file rule dropped) | `if resolved(lines, section):` → `if resolved(...) or any(CORRECTION in other and heading in other for other_path in files …)` | `c7_correction_other_file` | **killed** |
| M5 | treat an unparseable input as a pass (K16 reads no JSON; analogue = an unreadable scanned file skipped silently) | `lines, found, fenced_here = scan_file(path)` → `try: … except OSError: continue` | `c11_unreadable` | **killed** |

Exact patches:

```diff
# M1
         if fence is not None:
             if clauses(strip_quoted(line)):
                 fenced += 1
             continue
+        if fence is not None and clauses(strip_quoted(line)):
+            fenced += 1
         if HEADING_RX.match(line):

# M2
-    ("tbd", re.compile(r"\bTBD\b")),
+    ("tbd", re.compile(r"TBD")),

# M3
-        if CORRECTION in line and heading in line:
+        if CORRECTION in line:

# M4
-            if resolved(lines, section):
+            if resolved(lines, section) or any(
+                    CORRECTION in other and section["heading"][3:].strip() in other
+                    for other_path in files if os.path.isfile(other_path)
+                    for other in open(other_path, encoding="utf-8", errors="replace").read().split("\n")):

# M5
-        lines, found, fenced_here = scan_file(path)
+        try:
+            lines, found, fenced_here = scan_file(path)
+        except OSError:
+            continue
```

Observed outputs (mutant hashes in the table below):

```
$ python3 $S/k16_detector.py $S/mut/k16/M1.sh $S/fx/k16   # c1df283a…
case=c3_fenced_only_promise expected=1 actual=0 rc=1 verdict=fail
case=c4_fenced_pseudo_heading expected=1 actual=0 rc=1 verdict=fail
detector cases=11 failures=2 verdict=FAIL
$ python3 $S/k16_detector.py $S/mut/k16/M2.sh $S/fx/k16   # e055c0ed…
case=c5_near_token_tbd expected=1 actual=0 rc=1 verdict=fail
detector cases=11 failures=1 verdict=FAIL
$ python3 $S/k16_detector.py $S/mut/k16/M3.sh $S/fx/k16   # 848ec869…
case=c6_correction_wrong_heading expected=0 actual=1 rc=0 verdict=fail
detector cases=11 failures=1 verdict=FAIL
$ python3 $S/k16_detector.py $S/mut/k16/M4.sh $S/fx/k16   # 265faf0b…
case=c7_correction_other_file expected=0 actual=1 rc=0 verdict=fail
detector cases=11 failures=1 verdict=FAIL
$ python3 $S/k16_detector.py $S/mut/k16/M5.sh $S/fx/k16   # 417d4a53…
case=c11_unreadable expected=notclosed actual=1 rc=0 verdict=fail
detector cases=11 failures=1 verdict=FAIL
```

Secondary probe — every K16 mutant against the **real committed base export**:

```
$ for f in limbs/k16-pristine.sh mut/k16/M{1..5}.sh; do bash -c '. "$1"; check_k16 "$2"' _ "$f" "$S/base"; done
pristine payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
M1       payload=sections=505,promises=1,fenced=0,unresolved=1 closed=0
M2       payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
M3       payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
M4       payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
M5       payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
```

Not discriminating for K16 (base has no `Correction (round 43)` anywhere, so no mutant can resolve base's single
promise); the fixture detector is what kills them. M1's `sections=491→505` is the fence mutant counting four fenced
pseudo-headings in committed bytes — visible in the payload even though the verdict does not move.

## K17 — ExecK17ClaimsBefore.sh (sha `37a513ed…`, 591 lines)

| # | mutant | patch (pristine → mutant) | killed by | verdict |
|---|---|---|---|---|
| M1 | drop the exclusion | K17 has **no fence logic at all** (`grep -nE '```\|fence\|FENCE\|~~~'` → 0 hits); its only exclusion is the record-quotation exemption. Patch: `attribution()` returns `None` unconditionally | `q7_quoted_record` | **killed** |
| M2 | drop the whole-token boundary | `BOUND = set("A…z0…9_/-")` → `BOUND = set()` (feeds both `whole_tokens` and `present`) | `q4_near_token` | **killed** |
| M3 | accept a supersede line without the token | `if present(para, token) and re.search(r"supersed", …)` → `if re.search(r"supersed", …)` | `q3_erratum_other_token` | **killed** |
| M4 | accept a token from another round's control | after the cited-receipt set is built, append every `.ufo/waves/round-*/{c1-controls,c2-controls,final-gates,receipts}/*` | `q5_other_round_control` + real base export | **killed twice** |
| M5 | treat an unparseable claims.json as a pass | `except (ValueError, TypeError): parse_errors += 1; detail.append(…); continue` → `except (ValueError, TypeError): continue` | `q6_unparseable` | **killed** |

Exact patches:

```diff
# M1
 def attribution(text, pos, receipts):
     """Return the record path a token is quoted from, or None."""
+    return None
     window = text[max(0, pos - 240):pos]

# M2
-BOUND = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_/-")
+BOUND = set()

# M3
-            if present(para, token) and re.search(r"supersed", para, re.I):
+            if re.search(r"supersed", para, re.I):
                 return name

# M4
                     if rel and not is_record(rel):
                         receipts.append(rel)
+            try:
+                other_rounds = sorted(os.listdir(waves))
+            except OSError:
+                other_rounds = []
+            for other_round in other_rounds:
+                for cdir in RECEIPT_DIRS:
+                    cpath = os.path.join(waves, other_round, cdir)
+                    if not os.path.isdir(cpath):
+                        continue
+                    for cname in sorted(os.listdir(cpath)):
+                        if os.path.isfile(os.path.join(cpath, cname)):
+                            receipts.append(".ufo/waves/%s/%s/%s" % (other_round, cdir, cname))
             receipts = sorted(set(receipts))

# M5
         except (ValueError, TypeError):
-            parse_errors += 1
-            detail.append("K17 detail round=%s result=parse-error" % entry)
             continue
```

Observed outputs (final bytes `37a513ed…`):

```
$ python3 $S/k17_detector.py $S/mut/k17/M1.sh $S/fx/k17   # 5aa9af3c…
case=q7_quoted_record expected=1 actual=0 rc=1 payload=claims=1,tokens=2,verified=1,superseded=0,unbacked=1 verdict=fail
detector cases=10 failures=1 verdict=FAIL
$ python3 $S/k17_detector.py $S/mut/k17/M2.sh $S/fx/k17   # 2287c561…
case=q4_near_token expected=0 actual=1 rc=0 payload=claims=1,tokens=1,verified=1,superseded=0,unbacked=0 verdict=fail
detector cases=10 failures=1 verdict=FAIL
$ python3 $S/k17_detector.py $S/mut/k17/M3.sh $S/fx/k17   # d0846b3e…
case=q3_erratum_other_token expected=0 actual=1 rc=0 payload=claims=1,tokens=1,verified=0,superseded=1,unbacked=0 verdict=fail
detector cases=10 failures=1 verdict=FAIL
$ python3 $S/k17_detector.py $S/mut/k17/M4.sh $S/fx/k17   # 6a1f9e53…
case=q5_other_round_control expected=0 actual=1 rc=0 payload=claims=1,tokens=1,verified=1,superseded=0,unbacked=0 verdict=fail
detector cases=10 failures=1 verdict=FAIL
$ python3 $S/k17_detector.py $S/mut/k17/M5.sh $S/fx/k17   # f71b3c84…
case=q6_unparseable expected=0 actual=1 rc=0 payload=claims=2,tokens=1,verified=1,superseded=0,unbacked=0 verdict=fail
detector cases=10 failures=1 verdict=FAIL
```

Secondary probe — the same mutants against the **real committed base export** (the frozen claim requires K14–K19
open at `ab98fac9`; the base K17 line is `closed=0` with the routed RD42-8 unbacked token):

```
$ for f in limbs/k17-pristine.sh mut/k17/M{1..5}.sh; do bash -c '. "$1"; check_k17 "$2"' _ "$f" "$S/base"; done
pristine  claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
M1        claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
M2        claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
M3        claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
M4        claims=20,tokens=6,verified=6,superseded=0,unbacked=0 closed=1   <-- base flipped green
M5        claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
```

M4 is killed twice, on two independent detectors: the fixture `q5` and the committed base export. Widening the cited
receipt set to every round's controls turns the real RD42-8 defect green (`verified=2→6`, `unbacked=1→0`), which is
exactly the kill rule "at base every one of K14–K19 is open".

Method note (recorded because it cost a false survivor): M4's first patch widened `receipt_text` instead of `receipts`,
and **survived** — `hit = [rel for rel in receipts if rel in receipt_text and …]` iterates the cited set, so extra
`receipt_text` keys are unreachable. The delivered limb's "cited only" rule is therefore closed by construction; the
mutant has to widen `receipts` itself. That first patch is not part of the table.

## Restoration evidence

Pristine bytes were never edited in place: every mutant is a copy. Restoration was exercised anyway — mutate a work
copy, run the detector, restore the pristine bytes byte-identically, re-run:

```
$ for fam in k16 k17; do for i in 1..5; do
    cp mut/$fam/M$i.sh work/limb.sh;  python3 ${fam}_detector.py work/limb.sh fx/$fam   # mutated: FAIL
    cp limbs/$fam-pristine.sh work/limb.sh; cmp -s work/limb.sh limbs/$fam-pristine.sh  # restore
    python3 ${fam}_detector.py work/limb.sh fx/$fam                                      # restored: PASS
  done; done
k16 M1 killed_by_cases=2 restored-ok sha=d7c33c9efdcfb5ab detector cases=11 failures=0 verdict=PASS
k16 M2 killed_by_cases=1 restored-ok sha=d7c33c9efdcfb5ab detector cases=11 failures=0 verdict=PASS
k16 M3 killed_by_cases=1 restored-ok sha=d7c33c9efdcfb5ab detector cases=11 failures=0 verdict=PASS
k16 M4 killed_by_cases=1 restored-ok sha=d7c33c9efdcfb5ab detector cases=11 failures=0 verdict=PASS
k16 M5 killed_by_cases=1 restored-ok sha=d7c33c9efdcfb5ab detector cases=11 failures=0 verdict=PASS
k17 M1 killed_by_cases=1 restored-ok sha=37a513ed7dfbc8dd detector cases=10 failures=0 verdict=PASS
k17 M2 killed_by_cases=1 restored-ok sha=37a513ed7dfbc8dd detector cases=10 failures=0 verdict=PASS
k17 M3 killed_by_cases=1 restored-ok sha=37a513ed7dfbc8dd detector cases=10 failures=0 verdict=PASS
k17 M4 killed_by_cases=1 restored-ok sha=37a513ed7dfbc8dd detector cases=10 failures=0 verdict=PASS
k17 M5 killed_by_cases=1 restored-ok sha=37a513ed7dfbc8dd detector cases=10 failures=0 verdict=PASS
```

Mutant hashes (before/after of each probe):

```
c1df283ae6c27915ea70d37207faae113ded5c3fd0e965536130f3d6593f0bd7  k16 M1
e055c0ed8ba3d71d6766f34ff04c8a82cc7806dfa05a452cc2cc0aadb8ed9443  k16 M2
848ec869717dd22011b5231d71d3619c5c2913db8b0226f735966d7bd98bfb16  k16 M3
265faf0b5810c3cfde2cf9e0bf3a55fb1f036d751ed223610f2780a620e439ef  k16 M4
417d4a530beec75cf4acb7fb79e588e99e0a4d52cd223aca227b372ec3788bc6  k16 M5
5aa9af3c4ebe685d11057862ddf80d0764d440591a692f3dde4497d9943d62c8  k17 M1
2287c56109910cc4d73d552e7755181d3e3ad3f5570fe43febcb89e2afe6cd34  k17 M2
d0846b3e5d07cab8592cab0e09ce7e4eb2326f29c2f56c89938867cc36bacc36  k17 M3
6a1f9e533570ee9a7b0d2ec453d95a4007b4b7cfd645fa2c0b7d1e14da45ff7e  k17 M4
f71b3c84a19dc7cb6749f7807e41de6bfe6ec196ac064e7eecdb9221b27d4e5c  k17 M5
```

Pristine after the whole battery: `k16 d7c33c9e…`, `k17 37a513ed…` — identical to the delivered bytes.

## Verdict

**10/10 mutants killed** (K16 5/5 on the fixture detector; K17 5/5, with M4 killed by both the fixture detector and
the committed base export). Zero survivors, zero inconclusive.

## Findings (coverage; no contract change proposed)

1. **K17 has no fenced-block limb to mutate.** `grep -nE '```|fence|FENCE|~~~' ExecK17ClaimsBefore.sh` → 0 hits.
   Fixture `q10_fenced_cell_token` records what the delivered limb actually does: a `closed=10/12` inside a fenced
   block of a claims cell is extracted and graded (`tokens=1,unbacked=1 closed=0`) — the fence is not special. If the
   round wants a fenced exclusion in K17, that is a new requirement for the limb owner, not a mutation of existing
   behaviour. The nearest existing exclusion (record quotation) is M1 and it is load-bearing.
2. **K17's cited-receipt rule is closed by construction** (`hit` iterates `receipts`, not `receipt_text`). Good for
   M4-style drift; it also means the receipt map must be widened at `receipts` to change behaviour (see method note).
3. **K16 emits no payload line when a scanned file is unreadable.** `check_k16` on an unreadable
   `corpus/lessons/*.md` dies with `PermissionError` (traceback to stderr, rc=1, no `K16 payload=…` line) rather than a
   red payload. The detector scores this `notclosed` (pass, because it does not close), so no verdict changes here, but
   the suite contract says one `K<n> payload=…` line per check; an unreadable file in the export would break that line.
   Reported for the K16 owner/RevK16, not repaired here.
4. **The K16 real-base probe cannot discriminate** (base carries no `Correction (round 43)` line), so K16's kills rest
   entirely on the fixture battery. K17's real-base probe does discriminate and independently kills M4.
5. **Behavioral parity across K17 revisions:** `fe046218…`, `c1a123f5…`, `37a513ed…` produced identical detector and
   base-export output for pristine and for all five mutants; later revisions touched the header comment and the
   selftest driver only.

## Tooling / scratch

- No tool installed or upgraded this seat (nothing needed; pacman untouched).
- Scratch `S=/fast/scratch/hyaku/kasegi-r43/MutK16K17` (detectors, 21 fixture trees, base export, mutant copies) is
  removed at exit. Disk guard at start: `/fast/scratch/hyaku` 26% used, 601.0G free.
- No network fetch; no mutating git command (only read-only `git archive`, `git status`, `git log`, `git rev-parse`).
- Every command above was run in this seat; outputs are quoted verbatim.
