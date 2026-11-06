# MutEntryGate — r83 C2 entry gate, G6 tie limb

Attack seat (leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; all commands run from
there with `TMPDIR=/fast/scratch/hyaku/kasegi-r83/MutEntryGate/tmp`. No lane bytes were written;
only the two files named below were produced in the wave dir.

## Frozen bytes under test

| object | path | sha256 |
|---|---|---|
| r83 gate | `.ufo/waves/round-83/c2/entry-gate.py` | `42f4b2accf704455325f8d1eb8ca4ec21401e35397af7a36861c33a27ace6302` (12464 B) |
| r83 controls | `.ufo/waves/round-83/controls/c2-controls-r83.py` | `8ab95ec589855fdc6d3e86a9b520ab3960b9763ea17f5b905e160f8ae10904c5` |
| S116 entry (beat base) | `corpus/knowledge/osv-high-quality-record-import-bar.md` | `fdb24948ab97a6453dbe470667d20b51b12e805582d087d7bc8b33c91df340d9` |

Gate sha256 before and after all runs: identical (`env.txt`, `driver.out` `RESTORED` line).

## Method

- **D1 — selftest.** `python3 -B <gate>.py --selftest`; pass = rc 0 and the 12-case `got` map
  unchanged (`good: True`, the other eleven `False`).
- **D2 — controls.** A scratch copy of `c2-controls-r83.py` with `GATES["r83"]` repointed at the
  mutant's absolute path (`os.path.join(lane, abs)` keeps the absolute path). Command:
  `python3 -B controls-<k>.py --lane <lane> --work $S/work-<k>`. Detector = the seven
  `gate=r83` CONTROL lines (3 G6 forgeries, 4 admitted entries) compared character for character
  with the pristine baseline, rc included.
- **D3 — probe battery (diagnostic).** `tied_ok` on twelve hand-built claim bodies (0/1/2/3
  shared stems, absent cite line, two cites, the 5-vs-20 stem pair, a stopword-only quote, the
  `withdrawn` pair, the 3-vs-5 stem pair, the 3-letter pair) plus one full gate-shaped entry, run
  against the pristine module and every mutant. It decides whether a survivor is a real behavior
  change or a structural no-op; it is not a pass/fail detector.
- Baseline fidelity: pristine controls reproduce the frozen receipt
  `.ufo/waves/round-83/controls/c2-g6-controls-r83.txt` exactly (`matches_frozen_receipt=True`),
  and the unmodified controls script matches the copied harness (`True`). A restored-pristine
  control rerun after the mutants is identical to the first baseline (`same_as_first_baseline=True`).
- Each mutant was built from the pristine bytes by a single anchored substitution (asserted count
  = 1) and differs from pristine only in the lines shown in `mutants.diff`; every mutant file
  stayed in scratch and the scratch root is deleted before yield.

## Result — 16 mutants: 8 killed, 8 survived (6 behavior-changing undetected, 2 equivalent)

| # | mutant (change) | D1 selftest | D2 r83 rows changed | D3 probe delta | verdict |
|---|---|---|---|---|---|
| 1 | `tie2to1` — TIE_WORDS 2 -> 1 | ok | 0 | tie1 False->True | **SURVIVED-undetected** |
| 2 | `tie2to0` — TIE_WORDS 2 -> 0 | **FAIL** | 2 | tie0/1, stop, stem35, len3, gate_ok ->True | KILLED-selftest |
| 3 | `any_to_all` — `any()` -> `all()` | ok | 1 | twocites True->False, nocite False->True | KILLED-controls |
| 4 | `stem5to3` — stem cut 5 -> 3 letters | ok | 0 | stem35 False->True | **SURVIVED-undetected** |
| 5 | `stem5to20` — stem cut 5 -> 20 | ok | 3 | stem True->False | KILLED-controls |
| 6 | `stop_empty` — STOP emptied | ok | 0 | stop False->True | **SURVIVED-undetected** |
| 7 | `stop_plus_withdrawn` — STOP gains `withdrawn` | ok | 0 | withdrawn True->False | **SURVIVED-undetected** |
| 8 | `membership_dropped` — `n in by_line` dropped | ok | 0 | none | SURVIVED-equivalent |
| 9 | `membership_union` — cited line ignored, tie to section stem union | ok | 1 | absentcite False->True | KILLED-controls |
| 10 | `cite_not_stripped` — cite token not removed before stemming | ok | 0 | none | SURVIVED-equivalent |
| 11 | `nocite_true` — `tied_ok` True when no cite | ok | 0 | nocite False->True | **SURVIVED-undetected** |
| 12 | `untied_out_of_ok` — `untied == 0` dropped from `ok` | **FAIL** | 4 | gate_ok False->True | KILLED-selftest |
| 13 | `untied_not_printed` — `untied=` dropped from profile line | ok | 7 | profile-line | KILLED-controls |
| 14 | `ge_to_gt` — `>=` -> `>` (needs 3 stems) | **FAIL** | 6 | tie2, withdrawn True->False | KILLED-selftest |
| 15 | `word_min3` — word floor 4 -> 3 | ok | 0 | len3 False->True | **SURVIVED-undetected** |
| 16 | `word_min5` — word floor 4 -> 5 | **FAIL** | 1 | none | KILLED-selftest |

Exact per-mutant stdout, diffs and probe maps: `MutEntryGate-receipts/driver.out` and
`driver.json`; the anchored edits: `mutants.diff`; hashes: `mutants.sha256`.

### Expected detector vs what actually ran

| mutant | expected catch (pre-run) | actual |
|---|---|---|
| `tie2to1` | controls — if a row had exactly 1 shared stem | no such row → survived |
| `tie2to0` | selftest (`filler`) | killed, selftest |
| `any_to_all` | controls (S114's two-cite rule) | killed, controls |
| `stem5to3` | none (no 3-vs-5 separator in either detector) | survived |
| `stem5to20` | controls (admitted entries rely on the 5-letter fold) | killed, controls |
| `stop_empty` | none (STOP unexercised) | survived |
| `stop_plus_withdrawn` | none (STOP unexercised) | survived |
| `membership_dropped` | none (redundant while TIE_WORDS >= 1) | equivalent |
| `membership_union` | controls (`copyrule` shares words across sections) | killed, controls |
| `cite_not_stripped` | none (`s`/`txt` are under the 4-letter floor) | equivalent |
| `nocite_true` | none (G5 rejects a rule without a citation first) | survived |
| `untied_out_of_ok` | selftest (three G6-only negatives) | killed, selftest |
| `untied_not_printed` | controls (profile line, not verdict) | killed, controls |
| `ge_to_gt` | selftest (`good` has exactly 2 stems) | killed, selftest |
| `word_min3` | none (no 3-letter tie case) | survived |
| `word_min5` | selftest (`good` uses 4-letter stems) | killed, selftest |

### What killed each (decisive evidence)

- **tie2to0** — D1: selftest `filler` True, expected False. D2: the `filler` forgery and S115 flip
  from rc 1 / untied=1 to rc 0 / untied=0 (with the threshold at 0, any located cited line ties).
- **any_to_all** — D1 blind: every selftest rule has one cite. D2: S114 Claim 3 cites
  `S114.txt:35` and `S114.txt:60`; line 60 is not tied, so `all()` flips S114 to rc 1, untied=1.
- **stem5to20** — D2: S113 rc 0->1 (untied=3), S116 rc 0->1 (untied=1), `copyrule` untied 1->2.
  Admitted entries rely on the five-letter fold (`import`/`imported`), so removing it is visible.
- **membership_union** — D2: the `copyrule` forgery (Claim 2's rule replaced by Claim 1's, citing
  `S116.txt:25`) now passes rc 0 / untied=0, because Claim 1's rule words share `records` and
  `version` with Claim 2's quote at line 36. `crosscite` is still caught there only by vocabulary.
- **untied_out_of_ok** — D1: `filler`, `crosscite`, `copyrule` all True; D2: the three forgeries and
  S115 flip to rc 0 while their `untied` column stays 1.
- **untied_not_printed** — D1 blind (selftest compares booleans, not the line). D2: all seven r83
  lines lose `untied=`; pass/fail is unchanged, so this is killed only by the output contract.
- **ge_to_gt** — D1: `good` False, because Claim 1's rule shares exactly two stems (`clear`,
  `days`) with its quote. D2: untied counts inflate (copyrule 1->5, crosscite 1->4, filler 1->4,
  S115 1->2), and S113 and S116 both flip rc 0->1.
- **word_min5** — D1: `good` False (four-letter `blue`/`days` fall under a floor of 5). D2: S113
  rc 0->1.

### Survivors

**Behavior-changing, no detector (6).**

1. **`tie2to1`** (threshold below 2). Real at entry level: an S116 copy whose Claim 1 rule shares
   exactly one stem with its quote (`... on the record.`) is rc 1 / untied=1 under the frozen gate
   and rc 0 / untied=0 under the mutant (`consequence.out`, `forged/consequence-one-stem.md`).
   Nothing sits on that boundary: the 12 selftest cases pin >=2 and 0 but never 1, and the control
   set's negative rows pin zero overlap (the `filler` forgery; S115 Claim 2, whose intersection
   with its cited line `S115.txt:32` is empty — verified `inter {32: []}`) or a foreign line
   (`crosscite`, `copyrule`), never exactly one shared stem.
2. **`stem5to3`**. Probe `stem35` (quote `import records`, rule `improve recipe ...`): 0 matches at
   a five-letter cut, 2 at a three-letter cut. No detector contains a pair that separates 3 from 5.
3. **`stop_empty`**. Probe `stop` (a quote made only of stopwords, e.g. `this rule claims that
   text`): a rule can now tie on nothing but stopwords. The list is unexercised.
4. **`stop_plus_withdrawn`**. Probe `withdrawn`: a two-stem tie drops to one and fails. This is the
   sharpest coverage gap: `withdrawn` is the leading word of the S117 pin ids the round's C2 target
   quotes (`Q01-withdrawn-excluded`, `Q02-withdrawn-get`, `.ufo/waves/round-83/controls/
   c2-prefreeze-r83.txt`), so this mutation would silently delete tie signal in exactly the next
   entry's vocabulary and no detector would notice.
5. **`nocite_true`**. Probe `nocite` False->True. At gate level G5's citation requirement masks the
   verdict: a no-cite, >=8-word rule gives rc 1 / ruleless=1 / untied=1 pristine and rc 1 /
   ruleless=1 / untied=0 mutated (`consequence.out`) — visible only in the profile column, and no
   control row contains a no-cite rule.
6. **`word_min3`**. Probe `len3` (quote `sky ice`, rule `ice sky ...`): 0 matches at the 4-letter
   floor, 2 at 3. Three-letter content words are unexercised.

**Equivalent under the frozen constants (2).**

7. **`membership_dropped`** (`n in by_line` removed, absent line -> empty stem set). With
   `TIE_WORDS >= 1`, a non-empty intersection implies the cited line is in `by_line`, so the clause
   is redundant; it is load-bearing only at `TIE_WORDS = 0`, which D1 kills on the constant itself.
8. **`cite_not_stripped`**. For SIDs of the form `S<digits>`, the cite token's only alphabetic runs
   are `s` and `txt`, both under the four-letter floor, so removing the `re.sub` cannot change the
   stem set for any input this gate can see.

## Beat G6 — three forged rules pass

Scratch copies of the landed S116 entry with only Claim 1's `Falsifiable rule:` line replaced;
every span, quote, section, pin and G5 condition is preserved. Verbatim (`beatg6.out`; the forged
entries are in `MutEntryGate-receipts/forged/`):

```
FORGERY stuffed: "Falsifiable rule: this statement is written in our own words for this section
and cites (S116.txt:25) as the gate requires; the record was imported."
  r82 rc=0 ... ruleless=0 header=ok
  r83 rc=0 ... ruleless=0 untied=0 header=ok

FORGERY negated: "Falsifiable rule: contrary to the quote at (S116.txt:25), the described record
is never imported by OSV.dev, so the page's stated purpose is false."
  r83 rc=0 ... ruleless=0 untied=0 header=ok

FORGERY ownline-false: "Falsifiable rule: every record that OSV.dev imports under (S116.txt:25)
must first be withdrawn by its maintainer, and none may return."
  r83 rc=0 ... ruleless=0 untied=0 header=ok

CONTROL pristine r83 rc=0 ... untied=0 header=ok
```

All three pass: keyword stuffing (two quote words appended to a filler sentence), a rule that
negates its own quote, and a rule that cites its own line, reuses the quote's vocabulary
(`record`, `imports`) for a false claim about withdrawal. G5 also passes them (`ruleless=0`), so
G6 contributes nothing against this class.

**Limit (one sentence):** G6 is lexical — it admits any rule that shares two five-letter word
stems with the span on the line it cites, so keyword stuffing, a rule that negates its own quote,
and a rule making a false claim out of the quote's own words all pass.

## Coverage findings (routed; no contract change proposed)

- **R83-MEG-1 — the TIE_WORDS lower bound is unpinned.** No selftest case and no control row has
  exactly one shared stem; `tie2to1` changes no detector output while flipping a one-stem forged
  entry from rc 1 to rc 0. The negative rows pin 0 stems or a foreign line only. (S115 Claim 2
  already fails r83 as `untied=1` in the frozen receipt and is reproduced exactly — pre-existing
  behavior, not a new finding.)
- **R83-MEG-2 — the STOP list and the `withdrawn` stem are unexercised**, the latter on precisely
  the vocabulary of the S117/F59 target.
- **R83-MEG-3 — the no-cite branch of `tied_ok` is dead at gate level** because G5 rejects a rule
  without a citation; `nocite_true` survives, changing only the `untied` column.
- **R83-MEG-4 — the stem-cut and minimum-length boundaries are unexercised**: `import`/`improve`
  separates 3 from 5 and `sky`/`ice` separates the 4-letter floor from 3.
- Documents-only note: the two equivalent mutants show `n in by_line` and the cite-token `re.sub`
  cannot be killed by behavior at the frozen constants; they need a code-reading test or a
  `TIE_WORDS = 0` scenario.

Re-run everything (drivers are self-sufficient; they recreate scratch and the pristine copy):

```
S=/fast/scratch/hyaku/kasegi-r83/MutEntryGate
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR=$S/tmp python3 -B .ufo/waves/round-83/w1/MutEntryGate-receipts/driver.py       # 16 mutants, D1+D2+D3
TMPDIR=$S/tmp python3 -B .ufo/waves/round-83/w1/MutEntryGate-receipts/beatg6.py       # 3 forged rules
TMPDIR=$S/tmp python3 -B .ufo/waves/round-83/w1/MutEntryGate-receipts/consequence.py  # one-stem / no-cite entries
```

## Evidence and files written

Written:
- `.ufo/waves/round-83/w1/MutEntryGate.md` (this report)
- `.ufo/waves/round-83/w1/MutEntryGate-receipts/` — `driver.py`, `driver.out`, `driver.json`,
  `mutants.diff`, `mutants.sha256`, `beatg6.py`, `beatg6.out`, `beatg6.json`, `consequence.py`,
  `consequence.out`, `consequence.json`, `env.txt`, `forged/{beat-stuffed,beat-negated,
  beat-ownline-false,consequence-one-stem,consequence-nocite}.md`

No tooling installed or upgraded; no lane, corpus, instrument or sibling file modified; scratch
root removed before yield. Restoration evidence: lane gate sha256 unchanged
(`42f4b2ac...6302`), restored-pristine control rerun identical to baseline.
