# CritTokenRead — round 43, wave 1 (seat receipt)

- **Seat**: `CritTokenRead` (critic, leaf — no subagent dispatch, no swarm, no second judge).
- **Lane**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `ab98fac9dce87130bc4f66de89e30650d63943dc`,
  claims freeze commit `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`.
- **Item**: whole-token audit (R41) over every NEW counter this round — K14–K19 and the gate's rule ids.
  For each matcher, submit near-tokens and record whether it is accepted; a prefix/substring acceptance is a
  defect with the exact regex and the byte it wrongly matched. Receipt-only: no deliverable text to land.
- **Axes touched**: `depth:verifiability` (a token reader that accepts a mangled byte grades a claim the suite
  did not measure), `coverage` (the gate's rule-line grammar).

## Audited bytes (sha256 pinned; `corpus/instruments/r43-closure.sh` did not exist at audit time)

`ls corpus/instruments/r43-closure.sh` → `No such file or directory` (re-checked after the last probe run).
The K14–K19 matchers therefore live in the wave-1 limb deliverables, and the gate's rule ids in the landed
instrument. Every sha256 below is of the bytes I probe:

```
4a4945b0…c48d4c  .ufo/waves/round-43/w1/ExecK14Corrections.sh
14a195b1…7304e9  .ufo/waves/round-43/w1/ExecK15WaveNarrative.sh
d7c33c9e…f5a74cb .ufo/waves/round-43/w1/ExecK16Placeholder.sh
37a513ed…c7f348  .ufo/waves/round-43/w1/ExecK17ClaimsBefore.sh
3551a0fc…495a89e .ufo/waves/round-43/w1/ExecK18Transcript.sh
75f9552e…539e52f .ufo/waves/round-43/w1/ExecK19Freeze.sh
8b6f8493…71cc8e6 corpus/instruments/claim-package-check.py
04951ca0…b57b17  corpus/instruments/claim-package-selftest.py
```

(full digests in §7). Probe scratch `S=/fast/scratch/hyaku/kasegi-r43/CritTokenRead`, export
`git -C <lane> archive 4cb6d4ae… | tar -x -C $S/exp` (153 MB, no failures).

## 1. The mandated near-token matrix (what the seat asked for, verbatim)

| near-token | matcher | accepted? | observed |
|---|---|---|---|
| `corrections=330` | K14 `LIT_RX` | **as the literal `corrections=330`** (correct); it does **not** satisfy `corrections=33` | `literals=1,stale=0,live=corrections=330` (live=330) and `stale=1` (live=34) |
| `closed=10/120` | K17 `TOKEN_RX`+`BOUND` / K18 `CLOSED_RX` | no — extracted as its own token `10/120`, graded unbacked/unbound | `K17 …token=closed=10/120 …result=unbacked closed=0 rc=1`; `K18 …unbound=1 closed=0 rc=1` |
| `failures=10` | K18 `SUMMARY_RX` (needs the full `selftest cases=N failures=M`) | no — `selftest cases=19 failures=10` is unbound against a transcript with `failures=0` | `K18 …unbound=1 closed=0 rc=1` |
| `S0670` | C2 counting command `grep -rlE '^source: S067' corpus/knowledge \| wc -l` | **YES — DEFECT D6** (prefix; matched the bytes `S067` inside `S0670`) | `1` with only a `source: S0670` file present; bounded regex gives `0` |
| `R-FILESX` | selftest `_SELFTEST_RULE_RE` `^RULE\s+(\S+)\s+verdict=(pass\|fail)\b` | matched as rule id `R-FILESX` (not `R-FILES`), then **rejected** by `sorted(rule_lines)==sorted(_SELFTEST_RULES)` | `'RULE R-FILESX verdict=pass' -> ('R-FILESX','pass')`, set comparison false |
| `verdict=WELL-FORMEDX` | selftest `_SELFTEST_SUMMARY_RE` `verdict=(WELL-FORMED\|DEFECT)\b` | no — `\b` after `D` blocks `X` | `None`. **But `verdict=WELL-FORMED-extra` IS accepted** — DEFECT D7 |

## 2. Defects (exact matcher + the byte it wrongly matched)

### D1 — K14 `LIT_RX` / `whole()` treat `/` as a token boundary (prefix acceptance)
`ExecK14Corrections.sh:57` and `:75`:
```python
LIT_RX = re.compile(r"(?<![0-9A-Za-z_])(corrections|groups)=([0-9]+)(?![0-9A-Za-z_])")
def whole(text, lit):  # (?<![0-9A-Za-z_])<lit>(?![0-9A-Za-z_])
```
The boundary class omits `/`, which the r42 `TOKEN_BAD` set (`r42-closure.sh:346-348`, `set("0123456789/.=_" + letters)`)
and K17/K18's own `BOUND` both include. Byte wrongly matched: the `/` after the digits.

```
$ . ExecK14Corrections.sh; check_k14 <tree live=1>        # SCORECARD carries "corrections=1/9"
K14 payload=literals=1,stale=0,superseded=0,live=corrections=1,groups=0 closed=1      rc=0
$ check_k14 <tree live=1, SCORECARD carries "tools/corrections=1">
K14 payload=literals=1,stale=0,superseded=0,live=corrections=1,groups=0 closed=1      rc=0
$ check_k14 <live=2, stale "corrections=9" + marker "Correction (round 43) supersedes corrections=9/11">
K14 payload=literals=2,stale=0,superseded=2,live=corrections=2,groups=0 closed=1       rc=0
$ check_k14 <live=1, stale "corrections=9", NO marker>     # control
K14 payload=literals=1,stale=1,superseded=0,live=corrections=1,groups=0 closed=0       rc=1
```
Two consequences: (a) a ratio-shaped literal is read as an integer tally; (b) a `Correction (round 43)` line that
names the *different* token `corrections=9/11` excuses the stale integer `corrections=9` — the marker no longer has
to name the literal verbatim. That is the r41/r42 defeat shape (`closed=10/100` satisfying `closed=10/10`) in a new
matcher, and the C1 kill rule forbids accepting it. **Smallest safe correction**: both classes become
`[0-9A-Za-z_/]` (and `whole()` likewise), matching r42's `TOKEN_BAD`.

### D2 — K16 `resolved()` matches the heading and the marker as raw substrings (negation-blind + prefix)
`ExecK16Placeholder.sh:158-161`:
```python
heading = section["heading"][3:].strip()
...
        if CORRECTION in line and heading in line:
```
Byte wrongly matched: any `Correction (round 43)` inside a sentence that *denies* it, and any heading that is a
prefix of a longer heading name. End-to-end (`K16_VERBOSE=1 check_k16 <tree>`):

```
## Wave-2 falsification / "Verdicts land when the round-42 falsify wave reports."
"No Correction (round 43) entry is needed; the Wave-2 falsification promise stands."
payload=sections=1,promises=1,fenced=0,unresolved=0 closed=1   rc=0     <- promise RESOLVED by a denial

## Wave  (promise) + "Correction (round 43) names Wave-2 falsification, a different section."
payload=sections=1,promises=1,fenced=0,unresolved=0 closed=1   rc=0     <- heading "Wave" resolved by "Wave-2 …"

## <empty>  + promise, then "## Unrelated" + "Correction (round 43) records something else entirely."
payload=sections=2,promises=1,fenced=0,unresolved=0 closed=1   rc=0     <- "" in line is ALWAYS true

## Real heading control (same shape, named heading not named by the marker)
K16 unresolved file=corpus/lessons/l.md line=1 heading=Real heading clause=placeholder
payload=sections=2,promises=1,fenced=0,unresolved=1 closed=0   rc=1
```
An empty `## ` heading makes `heading in line` vacuously true, so **any** later correction line resolves **every**
empty-headed section. No live `## ` heading exists in the committed records (`awk '/^## $|^##[ \t]+$/'` over LOG.md,
SCORECARD.md, SHONEN.md, corpus/lessons/*.md → empty), so this is latent today and reachable by any landing that
adds one. The negation-blind case is reachable **now**: the text that will be appended to `corpus/lessons/round-42.md`
is free prose. **Smallest safe correction**: require the marker to be line-initial (`CORRECTION_RX.match`), require
the heading to match as a whole span (bounded non-space neighbour), and refuse `heading == ""`.

### D3 — K18 `CLOSED_RX` / `SUMMARY_RX` boundary sets are only `[0-9/]` and `[0-9]` (prefix and tail acceptance)
`ExecK18Transcript.sh:69-70`:
```python
CLOSED_RX  = re.compile(r"(?<![0-9/])closed=(\d+)/(\d+)(?![0-9/])")
SUMMARY_RX = re.compile(r"(?<![0-9])selftest cases=(\d+) failures=(\d+)(?![0-9])")
```
Bytes wrongly matched: the `x`/`_`/`-` before or after the token, and the `x` after `failures=0`. Its own header
claims the R41 boundary. End-to-end in a round-43 export whose only transcript prints `closed=19/19 exit=0`:

```
quoting line                                     result
closed=19/19 exit=0 (control)                    quotes=1,bound=1,unbound=0 closed=1  rc=0
xclosed=19/19 exit=0                             quotes=1,bound=1,unbound=0 closed=1  rc=0   <- prefix
field _closed=19/19 exit=0                       quotes=1,bound=1,unbound=0 closed=1  rc=0   <- prefix
value closed=19/19- exit=0                       quotes=1,bound=1,unbound=0 closed=1  rc=0   <- tail
paste artifact: closed=19/19x                    quotes=1,bound=1,unbound=0 closed=1  rc=0   <- the r42 probe's own reject case
selftest cases=19 failures=0x                    quotes=1,bound=1,unbound=0 closed=1  rc=0   <- tail
selftest cases=19 failures=10                    quotes=1,bound=0,unbound=1 closed=0  rc=1   (correct)
```
`closed=13/13x` is exactly the r42 `BOUNDARY_PROBES` reject pair (`r42-closure.sh:564`), so K18 accepts a mutant
built from the committed defeat bytes — the C1 kill-rule clause. **Smallest safe correction**: reuse r42's
`TOKEN_BAD` on both sides (`(?<![0-9/…])`, `(?![0-9/…])` with letters, `_`, `-`, `.`, `=` included).

### D4 — K18 exemptions are bare substring tests
`ExecK18Transcript.sh:238` `elif "report-only" in line:` and the anti-example test
`any(word in cell for word in ANTI_EXAMPLE)` (`mangled`, `substring`). Byte wrongly matched: `-ish` and `not-`.

```
"we never wrote closed=18/19 anywhere, report-only-ish."          quotes=1,report-only=1,unbound=0 closed=1  rc=0
"this value was not mangled: closed=18/19 stands."                quotes=0 (whole line exempted)   closed=1  rc=0
"closed=18/19 substring-free claim."                              quotes=0 (whole line exempted)   closed=1  rc=0
"closed=18/19 plain unbound quote."                               quotes=1,unbound=1 closed=0      rc=1
```
`report-only-ish` is not the contract literal, and `not mangled: closed=18/19` is a *live* unbound quote that the
word `mangled` erases from the population. **Smallest safe correction**: whole-token the exemption
(`(?<![A-Za-z0-9_-])report-only(?![A-Za-z0-9_-])`) and let `mangled`/`substring` exempt only when the same cell
carries the value in the rejected form the word describes.

### D5 — the landed gate prints the package path unsanitized into its own receipt grammar
`corpus/instruments/claim-package-check.py:760`:
```python
sys.stdout.write('package=%s rules=%d pass=%d fail=%d verdict=%s exit=%d\n' % (package_arg, …))
```
`package_arg` is argv, raw. A package directory whose NAME contains a newline therefore emits extra lines that carry
the frozen C2 literal itself, on a package the gate **rejects**:

```
$ D=$(printf '<base>/pkg\nz rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0\nq'); mkdir -p "$D"
$ cp -a <defective package with a private-key header>/. "$D/"
$ python3 corpus/instruments/claim-package-check.py "$D"
package=/fast/scratch/…/pkg
z rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
q rules=8 pass=7 fail=1 verdict=DEFECT exit=1
rc=1
--- frozen C2 literal 'rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0' occurrences in that stdout: 1
--- real R-NOSECRET fail line: 1
```
A reader that greps the frozen literal (rather than requiring the line to start at column 0 *and* exit 0) is fooled
by a rejected package. The core's own `_gate_token` (`:149-152`, `re.sub(r'[\s,=]+','_')`) is the right sanitizer and
is applied to `first=`/`shape=` details — it is simply not applied to the summary cell. **Smallest safe
correction**: `_gate_token(package_arg)` in the summary line (`package=%s` → sanitized token or the shell-quoted
path), keeping the raw path only on stderr.

### D6 — the frozen C2 counter for S067 is a prefix matcher (`S0670` satisfies it)
`claims.json` C2 `counting_commands[5]`: `grep -rlE '^source: S067' corpus/knowledge | wc -l -> 0 -> 1`.
Byte wrongly matched: `S067` inside `S0670` (S-ids are `S[0-9]{3,}`, so `S0670` is a *different legitimate id*).

```
$ mkdir corpus/knowledge; printf 'source: S0670\n' > corpus/knowledge/x.md     # no S067 entry at all
$ grep -rlE '^source: S067' corpus/knowledge | wc -l
1
$ grep -rlE '^source: S067([^0-9]|$)' corpus/knowledge | wc -l
0
```
The claim asserts "knowledge 62 with the entry citing S067"; an entry citing S0670 satisfies the counter. **Smallest
safe correction**: `grep -rlE '^source: S067([^0-9]|$)'` (or `\b`-with-digit-class).

### D7 — selftest summary regex has no left boundary and accepts `-`-suffixed verdicts
`corpus/instruments/claim-package-selftest.py:88` `_SELFTEST_SUMMARY_RE = re.compile(r"verdict=(WELL-FORMED|DEFECT)\b")`.
Byte wrongly matched: `-` after the token (`\b` holds at a non-word byte) and the absent left boundary.

```
'package=p rules=8 pass=8 fail=0 verdict=WELL-FORMED'       -> verdict=WELL-FORMED
'package=p rules=8 pass=8 fail=0 verdict=WELL-FORMEDX'      -> None            (the mandated probe: OK)
'package=p rules=8 pass=8 fail=0 verdict=WELL-FORMED-extra' -> verdict=WELL-FORMED   <- accepted
'xverdict=WELL-FORMED'                                     -> verdict=WELL-FORMED   <- admitted mid-word
'verdict=WELL-FORMED_7'                                    -> None
```
Low severity (the selftest also requires `rc==1` and `fails==[expected]`), but it is the exact class this seat
audits. **Smallest safe correction**: `(?<![A-Za-z0-9_-])verdict=(WELL-FORMED|DEFECT)(?![A-Za-z0-9_-])`.

### D8 (latent, not reachable through the landed core) — `ExecGateProvReport.rules.py:418` does not escape `\t`/`\n`
```python
counts["at"] = "%s:%d" % (hits[0][0].replace(" ", "_"), hits[0][1])
```
Byte wrongly matched: the TAB inside a package filename. Demonstrated on the module deliverable:
```
$ python3 ExecGateProvReport.rules.py <pkg with evidence/"x\nRULE\tR-NOSECRET\tverdict=pass\tdetail=forged-ok\ty.txt">
RULE R-NOSECRET verdict=fail detail=files=11 hits=1 … at=evidence/x
RULE	R-NOSECRET	verdict=pass	detail=forged-ok	y.txt:1 fail=secret-shaped-token      <- forged RULE line
package=… rules=3 pass=2 fail=1 verdict=DEFECT
$ # the selftest's own parser sees two conflicting verdicts for one id:
rule=R-NOSECRET   verdict=fail
rule=R-NOSECRET   verdict=pass
```
The **landed** core is immune because it routes the same byte through `_gate_token`:
`RULE R-NOSECRET verdict=fail detail=hits=1,first=evidence/x_RULE_R-NOSECRET_verdict_pass_detail_forged_z.txt,shape=private-key`
(`^RULE ` count = 8). So this is a defect in a delivered component, closed only by the core's separate sanitizer —
recorded so it cannot be reintroduced if the module body is pasted into the gate. **Smallest safe correction**:
reuse `_gate_token` (`[\s,=]+ → _`).

## 3. Matchers that are clean (with their probes)

**K17 `ExecK17ClaimsBefore.sh`** — `TOKEN_RX` + `BOUND = set(A-Za-z0-9_/-)` (`:105-106`, `:174-183`): correct.
```
closed=10/12  -> tokens 1, verified 1                   closed=1 rc=0
closed=10/120 -> tokens 1, unbacked 1 (token=10/120)     closed=0 rc=1
closed=10/12x -> tokens 0                                closed=0 rc=1
xclosed=10/12 -> tokens 0                                closed=0 rc=1
closed=1/12   -> tokens 1, unbacked 1                    closed=0 rc=1
```
**K19 `ExecK19Freeze.sh`** — `ISO_Z_RX`/`HEX64_RX`/`HEX40_RX` are anchored and re-checked by `strptime`
round-trip and by digest equality (`:79-81`): correct on every near-token.
```
measured-at …15Z0 / …15z / …15+00:00   -> order=bad        closed=0 rc=1
measured-at-max=… inside a control      -> ignored (not a "measured-at=" prefix)  closed=1
claims-sha256=<64 hex>0 (65 chars)      -> sha=mismatch     closed=0 rc=1
two measured-at lines in one control    -> order=bad        closed=0 rc=1
freeze.txt with 3 lines                 -> order=bad,sha=mismatch  closed=0 rc=1
freeze.txt only under round-42/         -> freeze=absent   closed=0 rc=1
```
**Gate rule ids** — the eight ids are constants (`_GATE_RULE_ORDER`/`RULES`, `:90-99`, `:698-705`); nothing matches them by
prefix. `grep -c '^RULE '` on the exemplar = 8 (`rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`, rc=0).

## 4. Named limits (not token defects — stated so they are not mistaken for coverage)

- **K16** grades only a section's opening stanza by design; a promise parked mid-section is invisible.
- **K18**'s evidence store is `.ufo/waves/round-42|43/`; a quote from an older round is outside its population.
- **K19** binds `claims.json` by digest but **not** the two control receipts: a forgery that backdates all four
  timestamps consistently passes —
  `frozen-at=2020-06-01…`, `measured-at-max=2020-01-02…`, both controls in 2020, digest recomputed →
  `K19 payload=freeze=present,order=ok,sha=match closed=1`. A second, *inline* (non-line-initial) `measured-at=`
  later than the maximum is also invisible (`closed=1`), because the limb requires a line to start with it.
- **K15** `SEATS = \b(\d{1,4})\s+seats\b` reads a comma-grouped count as its last group: `1,036 seats` → `36`,
  `2,236 seats` → `236`; and `NAMED` has no tail boundary, so `kasegi-r42-falsifyX` is read as wave
  `kasegi-r42-falsify`.

## 5. What the L1 should do (smallest safe corrections, in landing order)

1. D3 + D1 first: they are the two matchers that accept the r42/r41 defeat shape; both are a one-line boundary-class
   change. Rerun the limb's own transcript after the edit.
2. D2 (K16 marker + heading) before any correction text is appended to `corpus/lessons/round-42.md`; the negation
   case is reachable with the round's own prose.
3. D5 + D8 (gate output sanitization) before the gate is cited by any report line that greps its stdout.
4. D6: fix the frozen counting command's regex in the *report*, not in claims.json (claims.json is frozen); the
   command as written can be satisfied by an entry citing S0670.
5. D7 is cosmetic-but-cheap; D4 needs a rule decision (what "report-only" and "anti-example" mean as tokens).

## 6. Method (all runs are real; outputs above are verbatim)

Each matcher was exercised three ways where possible: (a) the Python regex lifted verbatim out of the delivered
bytes and driven over a literal probe list; (b) the limb's own entry point (`check_k14/15/16/17/18/19`) driven over
scratch trees built from the freeze export (`$S/exp`) plus one mutation each; (c) the landed CLI on a real package.
Trees were mutated one defect at a time, always with an unmutated control in the same batch. No check was inferred
from reading code alone.

## 7. Housekeeping

- **Tooling**: nothing installed or upgraded (no pacman/uv/npx/binary download); nothing written to any PATH
  directory; `~/.omp/agent/config.yml` and `mcp.json` untouched.
- **Scratch**: `S=/fast/scratch/hyaku/kasegi-r43/CritTokenRead/` created with `mkdir -p`, all exports/work copies
  bound there (`df` 25 % used; disk guard `status` clean); removed before this receipt was filed (`rm -rf -- "$S"`,
  verified absent).
- **Writes**: this receipt only — no lane file, no fleet-root file, no sibling lane, no source tree. No git/jj
  mutation anywhere (only `archive`, `rev-parse`, `log`, `show`, `status` were used).
- **Full digests of the audited bytes**:
```
4a4945b085d7f2a6e81dedbd195fe62ace214d4b0d000e2049acd3864cc48d4c  ExecK14Corrections.sh
14a195b1eb7ec61550bf4938f62ae7856dbae0c1a49dc7aba078f7b97304e93a  ExecK15WaveNarrative.sh
d7c33c9efdcfb5ab0feeac494da6a12d83d95d9b0d2d20b2bd121ba7af5a74cb  ExecK16Placeholder.sh
37a513ed7dfbc8dd83d6a77da2a44843ea424e0a932fb501bea681ccedc7f348  ExecK17ClaimsBefore.sh
3551a0fc5a18d9e94e4f3f11a07520f6fd8082842cafad00d1b98f862495a89e  ExecK18Transcript.sh
75f9552ec4958905b76c33f154ecaf0cdd099426d8bd0b321846167d8539e52f  ExecK19Freeze.sh
8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6  corpus/instruments/claim-package-check.py
04951ca0e72050725fc01a16ba1e42d7a52bd29bb0ae653b164a39ed39b57b17  corpus/instruments/claim-package-selftest.py
```
- **Inbound IRC**: `W1ScribeLessonGate` reported a `corpus/SOURCES.md` S242 pipe-escaping defect for whoever owns
  that row. Out of my write scope (receipt-only seat) and not acted on; no reply sent beyond noting it here.
