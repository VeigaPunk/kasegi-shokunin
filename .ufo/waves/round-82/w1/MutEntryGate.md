# MutEntryGate — r82 C2 entry gate, G5 content limb: mutation battery

Seat: mutation-tester. Scope: the NEW content limb G5 of
`.ufo/waves/round-82/c2/entry-gate.py` (frozen sha256 `1c5ddd52675b5aba5b5598023152779f307c2c3c2d84ddcae09ceec1c714058f`).
No lane file was written; all mutants are exact single-point replacements of a scratch copy.
Receipts: `MutEntryGate-receipts/` beside this report (mutants.txt = hashes + unified diffs,
mutants.json / entries.json = raw runs, the entry files themselves).

## 1. Frozen bytes and baseline

| object | sha256 |
|---|---|
| c2/entry-gate.py | `1c5ddd52675b5aba5b5598023152779f307c2c3c2d84ddcae09ceec1c714058f` |
| corpus/knowledge/osv-high-quality-record-import-bar.md | `1100997162fdd64b4282cd9b2afbe00f6549981733010e56cf6f39d2b1a30cac` |
| corpus/source-snapshots/round-82/manifest.json | `e0e4a246644ff4174d6724d9c73dd40c3674eb8a008a6209afc9b13e2e2f979b` |
| corpus/source-snapshots/round-82/S116.txt | `2198d329bf6a8711ac28ae9221351162d61679699c0b45acb8ebb95cadce9ca0` |
| r81 junk-labelled.md | `ba9e1e91948ff8b92ac400ababc562bc1ab7cf53a9824cd9662da2ba8fe5dcda` |
| r81 manifest.json | `7429df80bf425c8132b1325d0cd3b9e8527323f7e6eb61c31ce8b0774c5c05cf` |

Detectors, all run from `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` with lane-relative paths
(exactly predicate B8's invocation), `TMPDIR=/fast/scratch/hyaku/kasegi-r82/MutEntryGate`:

```
selftest  python3 -B <gate> --selftest                                             rc 0
junk      --entry .ufo/waves/round-81/w1/CriticClaims-receipts/junk-labelled.md \
          --manifest corpus/source-snapshots/round-81/manifest.json --source S115 rc 1
entry     --entry corpus/knowledge/osv-high-quality-record-import-bar.md \
          --manifest corpus/source-snapshots/round-82/manifest.json --source S116   rc 0
```

Baseline lines (`mutants.txt:12-15`):

```
selftest ok got={'good': True, 'dump': False, 'moved': False, 'norule': False, 'labelled': False, 'copied': False, 'snapline': False, 'nocite': False, 'shortrej': False}
junk  ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=6 header=ok
entry ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok
```

## 2. Mutant table (14 single-point mutants)

Every replacement asserted to occur exactly once in the base bytes (driver aborts otherwise).
`killed` = at least one detector moved off baseline; `SURVIVED` = all three identical to baseline.

| # | mutation (one point) | selftest | junk | entry | verdict |
|---|---|---|---|---|---|
| M01 | `MIN_WORDS = 8` -> `1` | **1** | 1 | 0 | killed (selftest) |
| M02 | `MIN_WORDS = 8` -> `7` | 0 | 1 | 0 | **SURVIVED** |
| M03 | drop the rej length test | **1** | 1 | 0 | killed (selftest) |
| M04 | drop the rule length test | 0 | 1 | 0 | **SURVIVED** |
| M05 | drop the cite regex | **1** | 1 | 0 | killed (selftest) |
| M06 | cite regex accepts any `.txt`, not the claimed SID | 0 | 1 | 0 | **SURVIVED** |
| M07 | drop the snapshot-substring test in `drawn_from_source` | 0 | 1 | 0 | **SURVIVED** |
| M08 | drop the manifest-quote test in `drawn_from_source` | **1** | 1 | 0 | killed (selftest) |
| M09 | reverse containment `line in text` | 0 | 1 | **1** | killed (entry) |
| M10 | drop the rej `drawn_from_source` call | 0 | 1 | 0 | **SURVIVED** |
| M11 | `label_text` returns the rest of the body, not the label line | 0 | 1 | 0 | **SURVIVED** |
| M12 | `ruleless` not in the `ok` conjunction | **1** | **0** | 0 | killed (selftest+junk) |
| M13 | missing labels count as content-ok | 0 | 1 | 0 | **SURVIVED** (equivalent) |
| M14 | drop the `^` anchor on the `Falsifiable rule:` label | 0 | 1 | 0 | **SURVIVED** |

Kill accounting: selftest 5 (M01, M03, M05, M08, M12), junk 1 (M12 only), entry 1 (M09).
**6/14 killed, 8/14 survived.** The junk fixture — the r81 labelled six-quote dump that G5 was
added to reject — kills exactly one mutant: the one that deletes the `ruleless` term from `ok`.
Its rules are empty, so any single surviving check still rejects it. The r82 B8 control pair
proves the limb *exists*; it does not exercise its clauses individually.

## 3. Survivors are real holes, not equivalent mutants

Each survivor got a witness entry: passes every other limb, rejected by the base gate, admitted
by the mutant. Witnesses are in `MutEntryGate-receipts/X-*.md`; all runs are `entries.json`.

| mutant | witness | base | mutant |
|---|---|---|---|
| M02 | 7-word rule `seven words sit right here now (S116.txt:25).` | rc1 `ruleless=1` | rc0 `ruleless=0` |
| M04 | 2-word rule `x (S116.txt:25).` | rc1 `ruleless=1` | rc0 `ruleless=0` |
| M06 | rule cites `(S999.txt:25)`, no S116 cite | rc1 `ruleless=1` | rc0 `ruleless=0` |
| M07 | rej is a verbatim substring of `S116.txt:33` | rc1 `ruleless=1` | rc0 `ruleless=0` |
| M10 | rej contains manifest quote Q03 | rc1 `ruleless=1` | M10 rc0, M07 rc1 |
| M11 | empty `Falsifiable rule:` label; the following rej line carries the cite | rc1 `ruleless=1` | rc0 `ruleless=0` |
| M14 | label mentioned mid-line in prose; the anchored label line is empty | rc1 `ruleless=1` | rc0 `ruleless=0` |
| M13 | claim with no labels at all | rc1 `claimless=1 ruleless=1` | rc1 `claimless=1` |

M13 is equivalent: `claimless` already requires both anchored labels, so `content_ok`'s
`rule is None or rej is None` guard is dead weight (redundancy, not a defect).
The other seven are live coverage gaps with a working witness.

## 4. Three worthless entries that PASS the unmutated gate

All three print `ruleless=0` / `ENTRY-GATE-RESULT pass`, rc 0 (`entries.json`, files in receipts):

| entry | construction | gate output |
|---|---|---|
| W1-boilerplate | the same 9-word generic rule under all six claims, only the line number changes; the same 11-word rej | `ENTRY-GATE sid=S116 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok` / `ENTRY-GATE-RESULT pass` |
| W2-copied-rules | the six rules of the S115 entry (`osv-importfindings-record-quality-feedback.md`) copied with the SID rewritten to `S116.txt:25/36/41/44/47/51`; they describe a different page and the cited lines do not support them | same line, `ruleless=0` / `pass` |
| W3-vacuous | `bananas are yellow and they grow in hanging bunches (S116.txt:25).` + `penguins cannot fly and they live in cold places.` | same line, `ruleless=0` / `pass` |

Two more limits found while probing (also pass, rc 0):

- **W4-duplicate-rule-rej** — the identical sentence under both the rule label and the rej label,
  six times. Nothing requires the two texts to differ.
- **W5b-source-prose-plus-cite** — the rule is 19 words of *verbatim* non-pinned source prose
  (`OSV.dev seeks to be a comprehensive, accurate and timely database of known vulnerabilities that
  is highly automation friendly (S116.txt:33).`). Verbatim source text passes as long as a cite is
  appended.

## 5. Structural findings (routed, not verdict changes)

1. **The rule-side snapshot-substring test is unreachable.** `content_ok` requires the rule to
   contain `(SID.txt:n)` *before* calling `drawn_from_source`; the snapshot contains no such
   literal (`grep -c 'S116\.txt:' S116.txt` = 0), so any rule that passes the cite test contains a
   token no snapshot line contains and can never be `text in line`. The snapshot branch is live
   only on the rej text — and no fixture exercises it there (M07/M10 survive). W5b is the proof.
   Fix shape: strip the cite before the substring test, or test each sentence of the rule.
2. **`snapline` in the selftest is confounded.** Its rule is a snapshot substring *and* carries no
   cite, so the cite test rejects it whether or not `drawn_from_source` works (M07 survives).
   A case needs both a cite and a snapshot-substring body.
3. **No selftest case has a rej drawn from source** (M10 survives); the rej half of
   `drawn_from_source` has zero fixture coverage.
4. **`MIN_WORDS` boundary untested** (M02 survives). The real entry's rules are 31-43 words and its
   rejs 22-35, so the 8-word floor is never near a boundary in the only real fixture.
5. **Wrong-SID cite untested** (M06 survives): no case cites a different source's `.txt`.
6. **The rule length test is subsumed in practice** (M04 survives): every empty rule also fails the
   cite test, so the length test only bites at 1-7 words, which no fixture has.
7. **`label_text`'s line scoping is untested** (M11 survives): an empty `Falsifiable rule:` label
   borrows the following line, so one sentence can satisfy both labels if it carries a cite.
8. **Label anchoring in `content_ok` is untested** (M14 survives): `claimless` still requires the
   anchored label, so the exploit needs the anchored label present-but-empty plus a prose mention.
9. **The cite is SID-only, not support-checking.** W2 passes with six rules from another page whose
   cites point at S116 lines that say nothing of the kind. This is inside the docstring's declared
   limit ("does not check that the rule is true or that it follows from the quote"), but it is the
   most plausible worthless entry and the one a reviewer should watch.

## 6. Restoration and hygiene

- The lane tree was never written: `entry-gate.py` sha256 `1c5ddd52…` before and after
  (`mutants.txt` header, `mutants.py` final line). All mutants and entries live under
  `/fast/scratch/hyaku/kasegi-r82/MutEntryGate/` and were deleted on exit.
- No tool installed, no pacman transaction, no git/jj write, no `/tmp` output.
- Commands run: the three detectors above per mutant, plus the witness/entry runs in `entries.py`.

**C2 B8 status from this seat:** the gate's pass on the real entry and its fail on the r81 labelled
dump both reproduce (baseline rc 0 / rc 1), so B8 as written holds. The content limb is weaker than
its docstring implies: 8/14 single-point mutations survive all three controls, and three
zero-information entries (plus two more) pass it. Routed to round 83 as findings 1-9 above.
