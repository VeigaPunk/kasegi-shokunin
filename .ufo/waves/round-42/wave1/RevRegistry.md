# RevRegistry — review of the SKILL.md registry repair plan (D-r41-3, family F-TABLE / J3)

Seat: RevRegistry-2 (reviewer, receipt-only). Base 5053a7f46de35784cff4b56756906e9014a38276, lane tip 0566bd6; `SKILL.md` untouched at review time (sha256 `f8e7a5d3be74699329162635b26731e0ce156483dc17bd29a3323eef15413e00`, 1129 lines). No installs, no network, no writes outside scratch + this receipt.

## Verdict

D-r41-3 verified exactly as filed. **But ExecJ3Registry's fix as specified will not make J3 green by itself**: three further registry defects exist that the spec's `check_j3` predicates (and the frozen J3 text) would flag. At review time ExecJ3Registry had not landed `.skill-fix.txt`/`.sh`/`.transcript.txt` (`ls wave1/` showed only `RevLessonShape.md`, `ScribeScorecard.round42.txt`, `swarm-registry.json`), so the "no row lost" check below is run against my own reference fix and a reusable checker (`chk.py`, inline at the end) that the L1 can point at ExecJ3Registry's bytes once it lands.

## 1. D-r41-3 defect, exact (SKILL.md at base)

- Blank line: **L1121** is empty; it sits between the Round-40 table separator **L1120** (`|---|---|---|---|---|---|---|---|`) and the only Round-40 row **L1122** (`| r40-closure.sh | gate | ...`). L1123 is blank, L1124 is the `## Round-41 ...` heading. Detector run: `blank-after-separator lines: [1120]`.
- Duplicate identity: rows **L1122** and **L1128** both have first cell `r40-closure.sh` (grep of table-row lines naming it: `[1122, 1128]`); L1128 sits in the Round-41 block (header L1126, sep L1127, then L1128 r40, L1129 r41-closure.sh).
- The two rows are NOT byte-identical (sha256 prefixes `303481cc9c` vs `ff6e6d5030`, 824 vs 816 bytes). Character diff: L1122 carries bare `|` inside backtick spans (`closed=0|1`, `exit=0|1`, `verdict=pass|fail`) — the unescaped pipes make it **11 cells in an 8-column table** — and a garbled tail `scratch/` --receipt-out` only`; L1128 is the sanitised form (`closed=0-or-1`, `pass-or-fail`, `scratch only`), 8 cells.
- Consequence for the fix: "keep the round-40 block row" (ExecJ3Registry spec) is only correct if the kept row is the **L1128 text moved to L1122**. Keeping L1122 verbatim leaves an 11-cell row that J3's own "bare internal pipes rejected" limb must reject (MutSkillTablePipes: `Bare pipe within entry command — Survived ok=1 cells=11`). The sibling instrument sha in both rows is the same (`bdbd18a3239c...`, 1734 lines) so the identity/provenance is unchanged.

## 2. Reference fix and no-row-lost check

Reference fix (scratch `fixed-min.md`, sha256 `c2c7e0bbcaca278503eb2d239a5519e72e68df6b5d2e39bf597b798590f016f3`, 1127 lines): (a) delete L1121; (b) replace L1122 by the L1128 text; (c) delete L1128. Resulting tail (L1119-1127): header, separator, `r40-closure.sh` row (contiguous), blank, Round-41 heading, blank, header, separator, `r41-closure.sh` row — the Round-41 block keeps its one required registration.

`python3 chk.py <file>` (inline below), actual output:

```
### ORIG
names lost: []            names added: []
closure scripts with 0 rows: []
closure scripts with >1 rows: {'r36-closure.sh': 2, 'r40-closure.sh': 2}
other >1 first-cell dups: {'anchorcheck.py': 2}
blank-after-separator lines: [1120]
rows w/ cells!=8 (8-col tables): [(981, 9), (982, 9), (1041, 9), (1054, 9), (1055, 9), (1122, 11)]
### FIXED-MIN
names lost: []            names added: []
closure scripts with 0 rows: []
closure scripts with >1 rows: {'r36-closure.sh': 2}
other >1 first-cell dups: {'anchorcheck.py': 2}
blank-after-separator lines: []
rows w/ cells!=8 (8-col tables): [(981, 9), (982, 9), (1041, 9), (1054, 9), (1055, 9)]
base rows byte-absent from cand: [(1122, 'r40-closure.sh')]   # only the broken variant
cand rows not byte-in base: []
```

So the reference fix loses no instrument name and no row except the garbled 11-cell r40 variant; all 8 `r*-closure.sh` scripts on disk (r-defect, r35-defect, r36..r41) keep >=1 row. Acceptance for ExecJ3Registry's bytes: `names lost: []`, `closure scripts with 0 rows: []`, `blank-after-separator lines: []`, `base rows byte-absent` limited to the r40 L1122 variant (and any intentionally edited rows below), `cand rows not byte-in base` limited to the r40 sanitised row and any intentionally escaped rows.

## 3. Findings (severity order)

**F1 — HIGH: fixing r40 alone leaves J3 red; the spec/claim predicates also hit rows nobody is fixing.** Run on FIXED-MIN:
1. `r36-closure.sh` has **two** registry rows (L1111 `gate\|probe`, verdict map `E<n> payload...`; L1113 `gate`, verdict map `0 closed \| 1 open \| 2 could-not-evaluate`, owner "round 36; D5 correction appended round 37"), both in the Round-36 block. ExecJ3Registry's own check ("every r*-closure.sh basename appears in exactly one registry row") fails on this at Y. It is not named in D-r41-3. The two rows are not duplicates: their verdict-map cells differ, so a merge must keep both verdict-map contents in one 8-cell row (no information loss) — or the check must be scoped to declare r36 a documented correction pair.
2. Five legacy rows carry bare `gate|probe` in the type cell → 9 cells in an 8-column table: **L981 recheck-audit.py, L982 anchorcheck.py, L1041 anchorcheck.py, L1054 frontier-recheck-count.py, L1055 source-recheck.py**. A J3 limb "bare internal pipes in a row's cells are REJECTED" applied to the whole registry (as the committed MutSkillTablePipes `cells=11` variant demands) is red on all five at Y. Either they are escaped (`gate\|probe`, same render as the post-r33 rows already use, e.g. L1064/L1097) or the check is scoped to blocks r36+ — the choice must be written into J3's replay limb, not discovered at receipt time.
3. `anchorcheck.py` has two rows (L982 round-26/28 state, L1041 round-29 state). L1041's own follow-on paragraph says "This row records the round-29 state of the same instrument as the row above (R6 append; no existing line moved)" — an intentional documented pair. The frozen J3 text (claims.json) says "no instrument basename appears in more than one row" with no scope; the ExecJ3Registry spec narrows it to `r*-closure.sh`. If the implemented J3 is the narrowed form, claims.json wording and implementation diverge and a literal-reading verifier finds `anchorcheck.py` twice at Y. Recommend the J3 payload line and the lesson state the scope (`corpus/instruments/r*-closure.sh` basenames) verbatim, or J3 applies the broader rule with a named, committed exemption list (anchorcheck.py L982/L1041 as R6 pair).

**F2 — MEDIUM: conflict with inherited append-only guards.** r41-closure.sh I12 (lines 1537-1586) fails when `git diff --numstat BASE Y -- SKILL.md PROVINCE.md` shows any deletion (`skdel -eq 0`), and r40-closure.sh H10 does likewise. Any landing of the F-TABLE fix deletes lines from SKILL.md (>= the blank line and the duplicate row; "modified" lines count as deletions). The frozen J12 is scoped to "no tracked deletions in corpus paths + density.py byte-identical" (SKILL.md is not under corpus/), so J12 is compatible **only if the J12 implementer does not port the `skdel==0` / PROVINCE append-only clause from I12**. The old suites (r40/r41) will necessarily read red on SKILL.md deletion at Y; that is expected (only r42 is claimed at Y), but J12 needs an explicit statement. Prior precedent: the round-41 verifier itself said "Repair the round-40 block or remove the duplicate next round" (spotcheck §5 D-r41-3) — repair-in-place is authorised.

**F3 — LOW/awareness: depth:density.** `density.py SKILL.md` mean block density at base 237.1 (780 path citations / 29 blocks) → 234.0 (777) with the reference fix (Round-40 block 7→6 rows..., Round-41 block 6→5 lines, density 340.0→250.0 for that block). Dropping the duplicate row can only lower the path-citation count. J12 pins `density.py` bytes (tool), not the measure, so the claim is not violated, but "harm none" on the owned axis depth:density is not strictly true; the L1 should decide knowingly (the alternative — keeping the duplicate — is the defect itself). Command: `python3 corpus/instruments/density.py <file> --label <x>` on `orig.md`/`fixed-min.md`.

**F4 — LOW: `check_j3` parser cautions.** (i) The L1064 row's first cell is `limb-mutation-check.py + limb-ledger.json` (two names in one cell): a "first cell == basename" test sees neither name; a substring test is needed for it (or it is out of scope for the closure-script rule). (ii) The 4-cell Frontier decision table (L1027-1033) and other pipe tables must be excluded — select registry tables by header `| name | type | entry command |` (8 columns), not by "any `|` line after L977". (iii) L1128's r41-closure.sh sibling row must still pass `registry_row_state` (prev line a table row/separator, header naming `name`, >=8 fields): verified by inspection of FIXED-MIN L1127 (`|---|` precedes it).

## 4. Recommendation to the L1 (what ExecJ3Registry's `.skill-fix.txt` must satisfy)

1. Remove blank L1121; make the Round-40 block's single row the sanitised L1128 text (8 cells); delete L1128 from the Round-41 block (keep `r41-closure.sh`).
2. Decide and encode, before the receipt run: r36 merge-or-declared-pair; 9-cell legacy rows escaped-or-scoped-out; anchorcheck.py pair exempt-or-scoped-out. Each choice appears in `check_j3` and in its REPLAY limb against the committed MutSkillTablePipes variants (blank line, bare pipe, leading whitespace, moved row).
3. Do not copy I12's SKILL.md `skdel` guard into J12.
4. Run `chk.py` (below) over the landed `SKILL.md` at Y; `names lost: []` and `closure scripts with 0 rows: []` are the no-row-lost gates.

## Checker used (scratch `chk.py`, sha256 `f4efaf55d65c6f387ec45d8812c3b141d083eec2a23de8a1d33d5bab5318220a`, 27 lines)

```python
import re,sys,glob,os
L='/home/vgpnk/Projects/shokunin/kasegi-shokunin'
base=open(L+'/SKILL.md',encoding='utf-8').read().split('\n')
cand=open(sys.argv[1],encoding='utf-8').read().split('\n')
sep=re.compile(r'\|(-+\|)+')
def rows(lines):
    out=[]
    for n,l in enumerate(lines,1):
        if n>=977 and l.startswith('|') and not sep.fullmatch(l) and not l.startswith('| name ') and not (4==len(re.split(r'(?<!\\)\|',l))-2):
            out.append((n,l))
    return out
def ident(l): return l.split('|')[1].strip().strip('`')
bn=[ident(l) for _,l in rows(base)]; cn=[ident(l) for _,l in rows(cand)]
print('names lost:',sorted(set(bn)-set(cn)))
print('names added:',sorted(set(cn)-set(bn)))
disk=sorted(os.path.basename(p) for p in glob.glob(L+'/corpus/instruments/r*-closure.sh'))
print('closure scripts with 0 rows:',[d for d in disk if cn.count(d)==0])
print('closure scripts with >1 rows:',{d:cn.count(d) for d in disk if cn.count(d)>1})
print('other >1 first-cell dups:',{k:cn.count(k) for k in set(cn) if cn.count(k)>1 and k not in disk})
bs=[n for n,l in enumerate(cand,1) if sep.fullmatch(l) and n<len(cand) and cand[n]=='' and n+1<len(cand) and cand[n+1].startswith('|')]
print('blank-after-separator lines:',bs)
print('rows w/ cells!=8 (8-col tables):',[(n,len(re.split(r"(?<!\\)\|",l))-2) for n,l in rows(cand) if len(re.split(r"(?<!\\)\|",l))-2!=8])
print('leading-ws first cells:',[n for n,l in rows(cand) if not l.startswith('| ') or l.split('|')[1]!=l.split('|')[1].strip().join([' ',' '])])
# row-content lost: non-identical rows from base absent in cand
bs_=set(l for _,l in rows(base)); cs_=set(l for _,l in rows(cand))
print('base rows byte-absent from cand:',[(n,ident(l)) for n,l in rows(base) if l not in cs_])
print('cand rows not byte-in base:',[(n,ident(l)) for n,l in rows(cand) if l not in bs_])
```

Usage: `python3 chk.py <candidate SKILL.md>`; it compares to the lane's current SKILL.md (base) and the instruments on disk.

## Provenance

Commands: `grep`-style row scans via python over `SKILL.md` L977-1129; `sed -n` of L1077-1129; reading `corpus/lessons/round-41-verifier-spotcheck.md` §5 item 3, `.ufo/waves/round-41/wave2/MutSkillTablePipes.md`, `corpus/instruments/r41-closure.sh` L1145-1215 and L1525-1590, claims.json J3/J12 text, wave1-spec.json ExecJ3Registry prompt. Tools installed: none. Scratch `/fast/scratch/hyaku/kasegi-r42/RevRegistry` removed before yield.
