# ReviewC1Sites — round-96 C1 tranche 11 (five non-author labels)

Seat scope: the five C1 edits in `.ufo/waves/round-96/c1/repair-map.tsv`, read against the
committed bytes of their anchors at the C1 landing `3c0581e2616df7a10af494a785b479d5e5293749`
(base `d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6`, freeze `804e7bc344df0808c880815dde077c28be5db18a`).
Read-only on the lane's git/jj state; no mutation.

## Verdict

**5/5 CORRECT, 0 PARTIAL, 0 WRONG.** Every new value is true of its anchor at the landing:
`SKILL.md:182-185` carries the completed round-13 `is_live(1)` correction (the parenthetical
closes on 185), `SKILL.md:182-185,255-257` is true of both ranges, the qualified
`corpus/source-snapshots/round-30/S041.txt:1680-1681` is in range (2354 lines) and carries the
no-contradiction sentence, and the two `(L...)` pointers land on d) 1832-1833 and e) 1834
(f) is 1835). The round-97 label set is empty: `ReviewC1Sites-receipts/round97-labels.tsv`.

I re-derived P1 myself (meter pass rc=0, every limb as frozen). I did **not** re-run the P2
control harness or re-derive P3, so this is AGREE on the five sites and on P1 — not a
claim-level STANDS.

## Row table

| # | site | key (label) | new text | verdict |
|---|---|---|---|---|
| 1 | `corpus/knowledge/triage-thresholds.md:88` | `SKILL.md:182-184` | `` `SKILL.md:182-185` `` | **CORRECT** |
| 2 | `corpus/knowledge/triage-thresholds.md:90` | `SKILL.md:182-184,255-257` | `` `SKILL.md:182-185,255-257` `` | **CORRECT** |
| 3 | `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:13` | `S041.txt:1680-1681` | `` `corpus/source-snapshots/round-30/S041.txt:1680-1681` `` | **CORRECT** |
| 4 | `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:36` | `d) information useful when submitting a possible vulnerability report (L1832-1834)` | `d) information useful when submitting a possible vulnerability report (L1832-1833)` | **CORRECT** |
| 5 | `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:36` | `e) out-of-scope services (L1835)` | `e) out-of-scope services (L1834)` | **CORRECT** |

## Per-row evidence

### Row 1 — `triage-thresholds.md:88` → `SKILL.md:182-185` — CORRECT

Anchor line (after, 3c0581e):

```
| curated | `rec.ev_inputs && Object.keys(rec.ev_inputs).length > 0` (boolean, not EV magnitude) | `1e12` = 1,000,000,000,000 | 107, 110 | SUPERSEDES: `SKILL.md:182-185` (round-13 correction: earlier text omitted `is_live(1)`) and `SKILL.md:255-257` (`curated` is a boolean on non-empty `ev_inputs`, never an EV magnitude); see §2.2 |
```

Cited anchor `SKILL.md:182-185` at 3c0581e:

```
182: Dispatch ordering (`buildQueue`, fleet-dispatch.mjs:88,110) is five-termed:
183: `priority(9e12) > continue(2e12) > curated(1e12, boolean on non-empty
184: ev_inputs) > reward.min×1000 > is_live(1)` (round-13 correction: earlier
185: text omitted `is_live(1)`) — exactly 1024 of 1088 records score 0 (796) or
```

The correction parenthetical opens on 184 (`(round-13 correction: earlier`) and closes on 185
(`text omitted `is_live(1)`)`). The old 182-184 cut the sentence mid-parenthetical; 182-185 is
the smallest range that completes it. TRUE.

### Row 2 — `triage-thresholds.md:90` → `SKILL.md:182-185,255-257` — CORRECT

Anchor line (after):

```
| freshness | `rec.freshness?.label === 'live' ? 1 : 0` | `1` | 110 | MATCHES: `corpus/knowledge/intake-surface.md:83-85`, `corpus/knowledge/mission-control.md:20-21`; SUPERSEDES: `SKILL.md:182-185,255-257` (round-13 correction: earlier text omitted `is_live(1)` and called `curated` an EV magnitude) |
```

Both ranges are true. 182-185 as in row 1. `SKILL.md:255-257` at 3c0581e:

```
255: curated(1e12) > reward.min×1000 > is_live(1) (round-13 correction: five
256: terms; `curated` is a boolean on non-empty `ev_inputs`, never an EV
257: magnitude) — EV orders, never gates (AR12). Dispatcher
```

255-257 carries both halves of the label's parenthetical: `is_live(1)` and "`curated` is a
boolean on non-empty `ev_inputs`, never an EV magnitude", closing on 257. TRUE of both ranges.

### Row 3 — `iso-29147…:13` → `corpus/source-snapshots/round-30/S041.txt:1680-1681` — CORRECT

Anchor line (after, tail of line 13):

```
… The guideline is explicit that the two frameworks have no major contradiction (§3, `corpus/source-snapshots/round-30/S041.txt:1680-1681`), so the difference is a gap in what is **required**, not a conflict in what is recommended.
```

Base line 13 carried the bare `` `S041.txt:1680-1681` `` at the same position; the edit adds
only the committed capture path. The file exists at that path and is 2354 lines, so 1680-1681
is in range. `S041.txt` 1679-1683:

```
1679: 3. 情報セキュリティ早期警戒パートナーシップと国際標準の関係
1680: これらの国際標準は、情報セキュリティ早期警戒パートナーシップの取組み
1681: と比較して、大きな矛盾や不整合はありません。したがって、情報セキュリテ
1682: ィ早期警戒パートナーシップガイドライン（以下、「P ガイドライン」という）
1683: に沿って脆弱性を取り扱っているベンダが国際標準に対応することも可能で
```

1680-1681 carries "これらの国際標準は、…比較して、大きな矛盾や不整合はありません" — the
quoted no-contradiction sentence, under heading §3 at 1679. TRUE. No bare `` `S041.txt:<n>` ``
token remains anywhere in `corpus/knowledge/` (all five S041 tokens there are path-qualified).

### Row 4 — `iso-29147…:36`, d) pointer `(L1832-1834)` → `(L1832-1833)` — CORRECT

### Row 5 — `iso-29147…:36`, e) pointer `(L1835)` → `(L1834)` — CORRECT

Anchor line (after):

```
- **6.2 Minimum policy aspects** (L1813) — Japanese 6.2 最小限の要素 (L1838). The minimum list has six lettered elements: a) how the vendor would like to be contacted (L1819), b) secure communication options (L1830), c) setting communication expectations (L1831), d) information useful when submitting a possible vulnerability report (L1832-1833), e) out-of-scope services (L1834), f) how submitted reports are tracked (L1835). Japanese rendering at L1842-1855.
```

`S041.txt` 1830-1835:

```
1830: b) Secure communication options
1831: c) Setting communication expectations
1832: d) Information that would be useful when submitting a
1833: possible vulnerability report
1834: e) Out-of-scope services
1835: f) How submitted reports are tracked
```

d) spans 1832-1833; 1834 is e) (the old pointer overran by one line). e) is 1834; 1835 is f)
(the old pointer overran by one line). Both new pointers land on their lettered items, and the
untouched f) pointer (L1835) is correct. TRUE.

M4 prose-pointer binding (the round-96 rule): for both rows the edited substring is exactly the
label key (`old == key`), the repair changes only the `(L...)` numbers
(`PTR.sub("", old) == PTR.sub("", new)`), and the new text introduces no backticked citation.
The meter's M4 pass confirms this mechanically; inspection agrees.

## Meter re-derivation (P1)

Command (receipts: `meter-rerun.txt`):

```
python3 -B .ufo/waves/round-96/c1/knowledge-meter.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --base-rev d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6 --after-rev 3c0581e2616df7a10af494a785b479d5e5293749 \
  --map .ufo/waves/round-96/c1/repair-map.tsv --labels-rev 804e7bc344df0808c880815dde077c28be5db18a \
  --base-target 1030/2027 --target 1032/2028 \
  --map-sha256 7d9bb49f366a594df3cd13e5651a6db4aabef1ab4b5a7081d89fd5f8c68b1d0f \
  --work /fast/scratch/hyaku/kasegi-r96/ReviewC1Sites
```

Observed rc=0:

```
KNOWLEDGE-METER base=1030/2027 after=1032/2028 base_target=1030/2027 target=1032/2028 sites=5 labels=5 after_rev=3c0581e2616df7a10af494a785b479d5e5293749 mirror_absent=True pinned=archive
LIMB M0 pass base=1030/2027
LIMB M1 pass after=1032/2028
LIMB M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0
LIMB M4 pass bad=none
LIMB M5 pass out_of_range=none
LIMB M9 pass rows=5 unbound=none
LIMB M10 pass labelled=5 want=5 mapped=5 kinds=part=4,range=1 unknown=none unapplied=none unlabelled=none
LIMB M6 pass sha256=7d9bb49f366a594df3cd13e5651a6db4aabef1ab4b5a7081d89fd5f8c68b1d0f
KNOWLEDGE-METER-RESULT pass rc=0
```

Token-level cause of the rate move (receipts: `token-diff.txt`) — exactly the five edits, no
side effect:

```
REMOVED 'S041.txt:1680-1681' GONE
ADDED   'SKILL.md:182-185' INTERNAL
ADDED   'corpus/source-snapshots/round-30/S041.txt:1680-1681' INTERNAL
```

Arithmetic: 1030/2027 − one GONE token (numerator unchanged) = 1030/2026; + `SKILL.md:182-185`
INTERNAL = 1031/2027; + qualified S041 INTERNAL = 1032/2028. Exactly the frozen target.

## Residual observations (not findings; none re-scores a claim)

1. `triage-thresholds.md:89` (reward row) still cites `SKILL.md:182-184`. Its own predicate is
   "the current queue tail writes `reward.min×1000`", which is on line 184, so the range is
   true for that predicate. No round-97 label.
2. `iso-29147…:55` keeps the prose pointer `(L1680-1681)`; S041 1680-1681 is the
   no-contradiction sentence, so it is true. No round-97 label.
3. `SCORECARD.md:3299` and `corpus/lessons/round-95*.md` quote the bare `S041.txt:1680-1681` in
   prose as the routed round-95 defect. They are reports, not citations, and sit outside the
   knowledge scope. No label.
4. The seat brief's parenthetical "(S041 1832-1834 and 1835)" describes the pre-edit targets.
   Committed bytes put d) at 1832-1833, e) at 1834, f) at 1835, and the new pointers match the
   bytes.

## Verification gaps

- P2 (12 controls, ATTRIBUTION fixtures=11) and P3 were not re-run/re-derived by this seat;
  they are outside the five-site scope.
- `mirror_absent=True`: classification is archive-pinned as the counter designs it; no host
  mirror was consulted.

## Receipts

All under `.ufo/waves/round-96/w1/ReviewC1Sites-receipts/`; lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

| command | rc | observed |
|---|---|---|
| `python3 -B .ufo/waves/round-96/c1/knowledge-meter.py … --after-rev 3c0581e… --work /fast/scratch/hyaku/kasegi-r96/ReviewC1Sites` (`meter-rerun.txt`) | 0 | `KNOWLEDGE-METER-RESULT pass rc=0`; M0 1030/2027, M1 1032/2028, M3 `bad_lines=0 old_not_once=0 dup_rows=0`, M4 `bad=none`, M5 `out_of_range=none`, M9 `rows=5 unbound=none`, M10 `labelled=5 want=5 mapped=5 kinds=part=4,range=1`, M6 frozen sha |
| `python3 -B /fast/scratch/…/tokdiff.py` (`token-diff.txt`) | 0 | `REMOVED 'S041.txt:1680-1681' GONE`; `ADDED 'SKILL.md:182-185' INTERNAL`; `ADDED 'corpus/source-snapshots/round-30/S041.txt:1680-1681' INTERNAL` |
| `git show 3c0581e:corpus/knowledge/triage-thresholds.md \| awk 'NR==88\|\|NR==89\|\|NR==90'` (`after-bytes.txt`) | 0 | 3 lines; :88 and :90 carry `SKILL.md:182-185` / `SKILL.md:182-185,255-257`; :89 unchanged |
| `git show 3c0581e:corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md \| awk 'NR==13\|\|NR==36'` (`after-bytes.txt`) | 0 | 2 lines; :13 carries the qualified S041 path; :36 carries `(L1832-1833)` and `(L1834)` |
| `git show 3c0581e:SKILL.md \| awk 'NR>=180&&NR<=190'` and `NR>=252&&NR<=260` (`skill-lines.txt`) | 0 | 182-185 and 255-257 quoted above; SKILL.md 1251 lines |
| `awk 'NR>=1679&&NR<=1683' / 'NR>=1812&&NR<=1836' / 'NR>=1838&&NR<=1855' corpus/source-snapshots/round-30/S041.txt` (`s041-lines.txt`) | 0 | 1680-1681 no-contradiction sentence; 1832-1833 d), 1834 e), 1835 f) |
| `git show d8a2bb0:…triage-thresholds.md \| awk 'NR==88\|\|NR==90'`; `git show d8a2bb0:…iso-29147….md \| awk 'NR==13\|\|NR==36'` (`base-map-labels.txt`) | 0 | base carries `SKILL.md:182-184`, `SKILL.md:182-184,255-257`, bare `S041.txt:1680-1681`, `(L1832-1834)`, `(L1835)` |
| `cat -A .ufo/waves/round-96/c1/repair-map.tsv`; `cat .ufo/waves/round-96/c1/labels.tsv` (`base-map-labels.txt`) | 0 | map rows carry backticks (row 3 old/new `` `S041.txt:1680-1681` `` / `` `corpus/source-snapshots/round-30/S041.txt:1680-1681` ``); labels 5 rows |
| `grep -rno '`S041\.txt:[0-9][0-9-]*`' corpus/knowledge/` (`bare-s041-scan.txt`) | 1 | `NONE`; all five S041 tokens in `corpus/knowledge/` are path-qualified |
| `git show 3c0581e --numstat`; `git diff --stat 3c0581e 7ef1d36` (`landing-scope.txt`) | 0 | landing: 2 files, 2+2 changed lines; C2 landing after C1 touches only `SCORECARD.md` and `corpus/instruments/capture-secret-scan.py` |
| `git diff --stat 53ec479 3c0581e -- SKILL.md`; `git show 804e7bc:.ufo/…/labels.tsv \| sha256sum`; `sha256sum` map/labels (`pins.txt`) | 0 | SKILL.md diff empty (line numbers stable since the label evidence); labels sha `757894d1…` at freeze and working tree; map sha `7d9bb49f…` = pin |

Round-97 label set: `round97-labels.tsv` (header only — no site wrong).
