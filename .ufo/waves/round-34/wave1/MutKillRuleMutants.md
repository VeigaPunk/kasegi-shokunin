# MutKillRuleMutants — round 34, wave 1 receipt

Seat: mutation-tester on `corpus/instruments/kill-rule-check.py` (C1's survivor-mutant counter).
Assignment: run the counter at the tip (expect `survivors=0`); introduce a non-killed mutant
(rule-B url-limb removal with different wording) and confirm the tool reports a survivor
(red-before for the obligation); confirm the three named mutants are genuinely killed.

All mutation work was done on scratch copies under
`/fast/scratch/hyaku/kasegi-r34/MutKillRuleMutants/` (deleted before yield). The lane files
were never edited by this seat; the only lane write is this receipt. No tools were installed
or upgraded (operator tooling authorization unused).

## Bytes verified

| file | sha256 | size |
|---|---|---|
| `corpus/instruments/capture-binding-check.py` (instrument under test) | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` | 40556 B / 892 lines |
| `corpus/instruments/kill-rule-check.py` (counter; §2–§8 measured at **generation 3**) | `7a20e724659ffa35ccce2f5072232c409e7b79d2e33fda878b5589c989d697f1` | 37730 B / 793 lines |
| `corpus/instruments/kill-rule-check.py` (counter, **latest observed, §12**) | `732e1e319298295709b3917fb0a9753192c0af455d912543deac82c513c88708` | (re-hashed during §12; gates 6 → 7) |
| `corpus/instruments/kill-rule-check.py` (counter, **FINAL, §13**) | `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` | 43138 B / 881 lines; 8 fixture probes + shape gate; sibling declares no edits after this |

The counter was a moving target while the sibling executor `ExecKillRuleCheck` landed it. Every
run below prints its own `KILL-RULE … counter_sha256=` header; the byte-move table is in
`ExecKillRuleCheck.md` §0: gen 1 `e33a300fc7341f8d6e254fc12441de1ba0ec6252483aeaf6e8806622dba0fc15`
(3 probes, 743 lines — what this seat first measured) → gen 2 `c51ac05a…` (intermediate) →
**gen 3 `7a20e724…` (6 probes — all primary figures below)**. Gen 3's probe set grew from
this seat's gen-1 survivor report (§8): the counter docstring records it
(`kill-rule-check.py:44-52`: "These five probes were added after an attack seat reported a
behaviour-bearing survivor (`unnamed-id-guard-removal`) at the three-probe generation; the two
siblings it named in the same report are pinned here too"). Two further generations were
observed while this seat finished (`b8e4fb4c…`, then `732e1e31…` — the probe set stays at six,
the gate count grows 6 → 7 with a new `named-rows` gate); §12 re-runs the tip command and the
survivor probe at `732e1e31…` and both verdicts hold. The instrument under test never
moved: `3d9e5e0d…` at first hash (05:31Z) and at final hash (05:57Z).

## Report

### 0. Independent harness (no counter code reused at run time)

Two scratch scripts written by this seat from the counter's documented probe contract:

- `detect.py` — replicates all SIX frozen-generation probes against an arbitrary instrument
  copy: `selftest-shape` (`--selftest` must print one `selftest case=…` line per case, a single
  `selftest cases=N failures=0` summary with N == case lines and N >= 19, every verdict=pass)
  plus five fixture lanes: `record-without-url` (url-less record → exit 1, `detail=absent`,
  `unbound=1`), `per-file-orphan` (undeclared capture → exit 1, `rule=orphan-capture`,
  `orphans=1 orphan=S009.txt`), `unnamed-record-id` (record with no `id` → exit 1,
  `rule=no-row record=<unnamed>`, `unbound=1`), `stale-orphan-declaration` (declared orphan
  absent → exit 1, `rule=orphan-declared-missing file=S077.txt`, `orphans=0`),
  `malformed-fetched-utc` (impossible UTC-shaped stamp + unparsable string → exit 1, both
  `record=S00x dir=round-32 detail=malformed`). Fixture builders replicate the counter's
  `build_*` shapes (`kill-rule-check.py:250-297`).
- `patch.py` — exactly-once patcher: `find` must occur exactly once (else exit 2), bytes must
  change (else exit 2), prints source/mutant sha256.

### 1. Pristine baseline — all six probes pass on the landed instrument

```
cp corpus/instruments/capture-binding-check.py cbc-live.py   # sha256 3d9e5e0d… (matches landed)
python3 detect.py cbc-live.py base
```

```
probe selftest-shape ok=1 exit=0
probe record-without-url ok=1 exit=1
  FAIL rule=url-mismatch record=S002 detail=absent dir=round-30
  records=2 bound=1 unbound=1
probe per-file-orphan ok=1 exit=1
  FAIL rule=orphan-capture file=S009.txt dir=round-30
  records=1 bound=1 unbound=0
probe unnamed-record-id ok=1 exit=1
  FAIL rule=no-row record=<unnamed> dir=round-30
  records=1 bound=0 unbound=1
probe stale-orphan-declaration ok=1 exit=1
  FAIL rule=orphan-declared-missing file=S077.txt dir=round-30
  records=1 bound=1 unbound=0
probe malformed-fetched-utc ok=1 exit=1
  FAIL rule=fetched-utc record=S001 dir=round-32 detail=malformed
  FAIL rule=fetched-utc record=S002 dir=round-32 detail=malformed
  records=2 bound=0 unbound=2
```

### 2. Counter at the frozen tip — `survivors=0`, exit 0

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/kill-rule-check.py --scratch "$S/kr-tip2" --json "$S/kr-tip2.json"; echo "tip_exit=$?"
```

Full stdout (exit 0):

```
KILL-RULE instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa bytes=40556 lines=892 floor=19 counter_sha256=7a20e724659ffa35ccce2f5072232c409e7b79d2e33fda878b5589c989d697f1
probe selftest-shape pristine=pass exit=0
probe record-without-url pristine=pass exit=1
probe per-file-orphan pristine=pass exit=1
probe unnamed-record-id pristine=pass exit=1
probe stale-orphan-declaration pristine=pass exit=1
probe malformed-fetched-utc pristine=pass exit=1
pristine selftest cases=23 case-lines=23 floor=19 floor_met=1
mutant-patch name=skip-selftest-summary patch_sha256=c457083e5d99f9f0 find_sha256=e6262244cffa1e1e find_count=1 status=ok
mutant-bytes name=skip-selftest-summary pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=b9d40dbee7521dbd
mutant-probe name=skip-selftest-summary probe=selftest-shape pristine=pass mutant=fail exit=0 reasons=summary-only;case-set-mismatch
mutant-probe name=skip-selftest-summary probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant=skip-selftest-summary killed=1
mutant-patch name=accept-record-without-url patch_sha256=83cbd622ad2fd1e2 find_sha256=cbf461982c746e9d find_count=1 status=ok
mutant-bytes name=accept-record-without-url pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=5897a1f044bcbf3f
mutant-probe name=accept-record-without-url probe=selftest-shape pristine=pass mutant=fail exit=1 reasons=exit=1;failures=1;case-verdict
mutant-probe name=accept-record-without-url probe=record-without-url pristine=pass mutant=fail exit=0 reasons=exit=0 want=1;missing='detail=absent';missing='unbound=1'
mutant-probe name=accept-record-without-url probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant=accept-record-without-url killed=1
mutant-patch name=per-file-binding-removal patch_sha256=f872ef12408d9162 find_sha256=f1a44079b9477ef2 find_count=1 status=ok
mutant-bytes name=per-file-binding-removal pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=616ce9dd0637a23b
mutant-probe name=per-file-binding-removal probe=selftest-shape pristine=pass mutant=fail exit=1 reasons=exit=1;failures=2;case-verdict
mutant-probe name=per-file-binding-removal probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=per-file-orphan pristine=pass mutant=fail exit=0 reasons=exit=0 want=1;missing='rule=orphan-capture';missing='orphans=1 orphan=S009.txt'
mutant-probe name=per-file-binding-removal probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant=per-file-binding-removal killed=1
control=CTL-noop verdict=invalid:noop expect=invalid:noop ok=1
control=CTL-nocompile verdict=invalid:nocompile expect=invalid:nocompile ok=1
control=CTL-equivalent verdict=survivor expect=survivor ok=1 witness_survivors=1 witness_exit=1
control=CTL-fake-killrule verdict=opaque expect=opaque ok=1 fake=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-34/c1-controls/fake-killrule.py fake_exit=0 fake_mutant_lines=0 fake_patch_digests=0 fake_mutants_line=0 fake_survivors=0 real_mutant_lines=3 witness_survivors=1 differs=1 stable=1
controls=4 rejected=4
GATE ok name=pristine-selftest
GATE ok name=pristine-fixtures
GATE ok name=pristine-determinism
GATE ok name=rows-valid
GATE ok name=controls
GATE ok name=survivors-zero
mutants=3 killed=3 survivors=0 invalid=0
gates=6 failed=0
survivors=0
tip_exit=0
```

C1's counting command `python3 corpus/instruments/kill-rule-check.py -> survivors=K` prints
`survivors=0` at exit 0 on the frozen bytes: all six gates ok, all four controls in their
expected verdicts, including `CTL-fake-killrule verdict=opaque … differs=1` — the do-nothing
fake runner `.ufo/waves/round-34/c1-controls/fake-killrule.py` (prints `survivors=0` without
replaying any mutant) is rejected as evidence on both counts.

### 3. Counter `--selftest` — green at the frozen bytes

```
python3 corpus/instruments/kill-rule-check.py --selftest; echo "selftest_exit=$?"
```

```
selftest case=all-killed got=(3, 0, 0, 0) want=(3, 0, 0, 0) verdict=pass
selftest case=one-survivor got=(2, 1, 0, 1) want=(2, 1, 0, 1) verdict=pass
selftest case=one-invalid got=(2, 0, 1, 1) want=(2, 0, 1, 1) verdict=pass
selftest cases=3 failures=0
selftest_exit=0
```

(The gen-1 draft's `one-invalid want=(1,0,1,1)` inconsistency — reported by peer
MutSelftestSummary — is fixed in the frozen bytes: `summarise()` counts exact `"killed"`
matches, so `["killed","invalid:find-count","killed"]` correctly yields killed=2.)

### 4. The three named mutants are genuinely killed (independent replay + tool replay)

Each named mutant was re-derived from the counter's own row spec with the independent
`patch.py` (exactly-once find, bytes changed) against the pristine copy, `py_compile`d, then
probed with the six-probe `detect.py`. Mutant byte digests match the counter's own
`mutant-bytes` lines — the counter's patches are byte-identical to the independent
reproductions:

| mutant | mutant sha256 (independent = counter) | killed by (six-probe detect.py) |
|---|---|---|
| `skip-selftest-summary` | `b9d40dbee7521dbd9e492655df734e062fde69f43b3333df1b1227c7a3becc97` | `selftest-shape` only: `ok=0 exit=0 reasons=summary-only;cases=0<floor=19`; all five fixture probes pass — the kill rests on the shape gate alone, as the counter documents |
| `accept-record-without-url` | `5897a1f044bcbf3fe90e21f8222a5336bd5b604dfe897fed16cbea6721b688b7` | `selftest-shape` (`exit=1;failures=1;case-verdict`; case `record-without-url` red: `exit=0 want=1`, missing FAIL line and summary) **and** `record-without-url` fixture (`exit=0 want=1;missing='detail=absent';missing='unbound=1'`, prints `records=2 bound=2 unbound=0` — the round-33 plain-run survivor shape, now caught) |
| `per-file-binding-removal` | `616ce9dd0637a23b8738ee1ae97e0668319507a828dfbb212536c79b6a8769cd` | `selftest-shape` (`failures=2`: cases `per-file-orphan-detected` and `per-file-orphan-listed` red — the mutant also drops the `orphans.append`, so the listed case's `orphans=1 orphan=S009.txt` substring goes missing too) **and** `per-file-orphan` fixture (`exit=0 want=1;missing='rule=orphan-capture';missing='orphans=1 orphan=S009.txt'`, AUDIT shows `orphans=0`) |

m2's independent detect.py output (m1/m3 in the table; full outputs measured and recorded in
this seat's transcript):

```
probe selftest-shape ok=0 exit=1 reasons=exit=1;failures=1;case-verdict
  selftest problem=exit=0 want=1 case=record-without-url
  selftest problem=missing='FAIL rule=url-mismatch record=S002 detail=absent dir=round-30' case=record-without-url
  selftest problem=missing='records=2 bound=1 unbound=1' case=record-without-url
probe record-without-url ok=0 exit=0 reasons=exit=0 want=1;missing='detail=absent';missing='unbound=1'
  records=2 bound=2 unbound=0
probe per-file-orphan ok=1 exit=1
  FAIL rule=orphan-capture file=S009.txt dir=round-30
  records=1 bound=1 unbound=0
probe unnamed-record-id ok=1 exit=1
  FAIL rule=no-row record=<unnamed> dir=round-30
  records=1 bound=0 unbound=1
probe stale-orphan-declaration ok=1 exit=1
  FAIL rule=orphan-declared-missing file=S077.txt dir=round-30
  records=1 bound=1 unbound=0
probe malformed-fetched-utc ok=1 exit=1
  FAIL rule=fetched-utc record=S001 dir=round-32 detail=malformed
  FAIL rule=fetched-utc record=S002 dir=round-32 detail=malformed
  records=2 bound=0 unbound=2
```

Verdict: **all three named mutants killed** at the frozen bytes, by the tool's own replay (§2:
three `mutant=… killed=1` lines) and independently. Every kill is a probe the pristine bytes
pass being failed by the mutant bytes; no kill rests on an invalid row (`invalid=0` everywhere;
every patch `find_count=1 status=ok`).

### 5. Run A — the tasked example mutant (rule-B url-limb removal, different wording): KILLED, not a survivor

The tasked red-before example was "rule-B url-limb removal with a different wording the tool
misses". Fed through the sanctioned `--row-file` mechanism (no tool edit): the mutant removes
the same url-required limb the counter's row 2 removes, but via a different, smaller textual
patch — only the limb's return line, not the counter row-2 three-line find block:

```
find    = "        return False, [\"rule=url-mismatch record=%s detail=absent\" % record_id]\n"
replace = "        return True, []  # mutant: url-required limb dropped, wording differs from row 2\n"
```

```
python3 corpus/instruments/kill-rule-check.py --scratch "$S/kr-runA" --row-file "$S/r4-url-limb-different-wording.json" --json "$S/kr-runA.json"; echo "runA_exit=$?"
```

Extra-row section and aggregates at the frozen bytes (the three named rows: identical to §2,
all killed=1; full stdout captured):

```
mutant-patch name=url-limb-different-wording patch_sha256=fe098c59869b2092 find_sha256=56d29fc6cf379f5a find_count=1 status=ok
mutant-bytes name=url-limb-different-wording pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=64c4d5863f9b3bf3
mutant-probe name=url-limb-different-wording probe=selftest-shape pristine=pass mutant=fail exit=1 reasons=exit=1;failures=1;case-verdict
mutant-probe name=url-limb-different-wording probe=record-without-url pristine=pass mutant=fail exit=0 reasons=exit=0 want=1;missing='detail=absent';missing='unbound=1'
mutant-probe name=url-limb-different-wording probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=url-limb-different-wording probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=url-limb-different-wording probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=url-limb-different-wording probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant=url-limb-different-wording killed=1
…
GATE ok name=survivors-zero
mutants=4 killed=4 survivors=0 invalid=0
gates=6 failed=0
survivors=0
runA_exit=0
```

Independent confirmation (patch.py + detect.py, mutant sha256
`64c4d5863f9b3bf39f6fce3977f04a23315423b687b2e08444c18a3e1d9b8535`): `selftest-shape ok=0`
(case `record-without-url` red) and `record-without-url ok=0 exit=0 … records=2 bound=2
unbound=0`; the other four probes pass.

**Finding (expectation discrepancy, reported not smoothed over):** the tasked example mutant is
**killed=1**, not a survivor, at every generation measured. The counter's probes are behavioral
(the tightened selftest report plus external fixture lanes), so a rule-B limb removal is caught
regardless of the wording its patch uses; "different wording the tool misses" only escapes the
counter's *matrix*, not its *probes*. The counter is stronger than the tasked example assumed.
Consequence: this mutant cannot serve as the red-before; §7 delivers the red-before the
assignment asks for.

### 6. Run B — the gen-1 survivor is closed at the frozen generation

Gen-1 finding (see §8): `unnamed-id-guard-removal` — drops rule B's unnamed-id diagnostic limb
(`rule=no-row record=<unnamed>`); an unnamed record then fails as `rule=no-row record=None`
via the fall-through id lookup. At gen 1 (three probes) it survived: no selftest case builds an
unnamed record and neither fixture probe exercised the input.

At the frozen gen-3 bytes the counter pins that limb with the `unnamed-record-id` fixture
probe. Tool replay (no tool edit; row fed via `--row-file`):

```
python3 corpus/instruments/kill-rule-check.py --scratch "$S/kr-runB" --row-file "$S/r5-unnamed-id-guard.json" --json "$S/kr-runB.json"; echo "runB_exit=$?"
```

```
mutant-patch name=unnamed-id-guard-removal patch_sha256=43e05bb83db62456 find_sha256=5185ff1a60486884 find_count=1 status=ok
mutant-bytes name=unnamed-id-guard-removal pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=9c46aeeec4f4858b
mutant-probe name=unnamed-id-guard-removal probe=selftest-shape pristine=pass mutant=pass exit=0
mutant-probe name=unnamed-id-guard-removal probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=unnamed-id-guard-removal probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=unnamed-id-guard-removal probe=unnamed-record-id pristine=pass mutant=fail exit=1 reasons=missing='rule=no-row record=<unnamed>'
mutant-probe name=unnamed-id-guard-removal probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=unnamed-id-guard-removal probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant=unnamed-id-guard-removal killed=1
…
GATE ok name=survivors-zero
mutants=4 killed=4 survivors=0 invalid=0
gates=6 failed=0
survivors=0
runB_exit=0
```

Independent confirmation (six-probe detect.py, mutant sha256
`9c46aeeec4f4858b5ee4741e8b0da08f56cec63c70eaf51cad8e5f35e24fed8d`): `unnamed-record-id ok=0
exit=1 reasons=missing='rule=no-row record=<unnamed>'` — the mutant prints
`FAIL rule=no-row record=None dir=round-30` where the probe wants `<unnamed>`; the other five
probes pass. **Closure verified: the gen-1 survivor is killed at the frozen bytes, by the probe
that pins its limb and by that probe only** (`selftest-shape` shows `mutant=pass`).

### 7. Run C — red-before at the frozen bytes: a behavior-bearing mutant the six probes cannot see is reported as a survivor

Mutant `url-token-normalization-removal`: drops rule B's URL-token normalization limb —
`row_tokens` stops stripping trailing `.,;:` from the registry row's `https://` token. A
registry row whose URL cell ends in punctuation would then mismatch its record's clean `url`
(the instrument would raise a false `rule=url-mismatch` on that live-tree shape). Every fixture
URL in every probe and every selftest case is clean, so no probe input changes: the mutant is
invisible to all six probes while being real behavior.

```
find    = "    return [token.rstrip(\".,;:\") for token in URL_TOKEN.findall(cell)]\n"
replace = "    return [token for token in URL_TOKEN.findall(cell)]  # mutant: trailing-punctuation normalization dropped\n"
```

```
python3 corpus/instruments/kill-rule-check.py --scratch "$S/kr-runC" --row-file "$S/r6-url-token-normalization.json" --json "$S/kr-runC.json"; echo "runC_exit=$?"
```

```
mutant-patch name=url-token-normalization-removal patch_sha256=1f72a07707bd0245 find_sha256=0dc5098846fd7602 find_count=1 status=ok
mutant-bytes name=url-token-normalization-removal pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=2e1ba326bd1a9d90
mutant-probe name=url-token-normalization-removal probe=selftest-shape pristine=pass mutant=pass exit=0
mutant-probe name=url-token-normalization-removal probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant=url-token-normalization-removal killed=0
control=CTL-equivalent verdict=survivor expect=survivor ok=1 witness_survivors=1 witness_exit=1
control=CTL-fake-killrule verdict=opaque expect=opaque ok=1 … differs=1 stable=1
controls=4 rejected=4
GATE ok name=pristine-selftest
GATE ok name=pristine-fixtures
GATE ok name=pristine-determinism
GATE ok name=rows-valid
GATE ok name=controls
GATE fail name=survivors-zero
mutants=4 killed=3 survivors=1 invalid=0
gates=6 failed=1
survivors=1
runC_exit=1
```

Independent confirmation (six-probe detect.py, mutant sha256
`2e1ba326bd1a9d908553b2f57f4e06b59b67850ded90f7785640d96415fdea04`): all six probes `ok=1`
— identical to the §1 baseline.

**Red-before confirmed at the frozen bytes:** the counter is not an always-zero printer. When a
mutant survives, it prints `mutant=url-token-normalization-removal killed=0`,
`mutants=4 killed=3 survivors=1`, `GATE fail name=survivors-zero`, and exits 1 — C1's kill-rule
conjunct ("kill-rule-check prints survivors>0") fires exactly as frozen. This is the
behavior-bearing version of the red-aggregate the counter's own `CTL-equivalent` witness
demonstrates on every run (`witness_survivors=1 witness_exit=1`, a comment-only patch); the
sibling's receipt §7 additionally records its own comment-only row
(`mutant=attack-comment-only killed=0`, `survivors=1`, exit 1).

### 8. Generation history — the gen-1 red-before that triggered the hardening

Measured at gen 1 (`e33a300f…`, 3 probes: selftest-shape, record-without-url, per-file-orphan),
before the sibling hardened the counter in response:

- Tip run at gen 1: `survivors=0`, `mutants=3 killed=3`, `gates=6 failed=0`,
  `controls=4 rejected=4`, exit 0 — same three named mutants, same mutant byte digests as §4.
- Tasked example (§5's mutant): already killed at gen 1 (same two probes).
- **Gen-1 red-before delivered** — `unnamed-id-guard-removal` fed via `--row-file`:
  all three probes passed on the mutant bytes, and the tool printed:

```
mutant=unnamed-id-guard-removal killed=0
GATE fail name=survivors-zero
mutants=4 killed=3 survivors=1 invalid=0
gates=6 failed=1
survivors=1
runB_exit=1
```

That survivors=1/exit-1 run is what the sibling cites as the reason the probe set grew
(`kill-rule-check.py:44-52` docstring; `ExecKillRuleCheck.md` §0 byte-move table
`e33a300f` → `c51ac05a` → `7a20e724`). The gen-1 coverage finding is therefore closed at the
frozen bytes (§6), and the red-before obligation is re-demonstrated at the frozen bytes by §7.

### 9. Coverage findings for the L1 (surviving mutant = gap, contract untouched)

1. **Probed at the frozen bytes — CLOSED at the final bytes (§13):** `url-token-normalization-removal` (§7) survived all
   six probes at gen 3/gen 5. The `row_tokens` trailing-punctuation normalization limb
   (`capture-binding-check.py:96`, `return [token.rstrip(".,;:") …]`) was pinned by no probe
   input — every fixture and selftest URL is clean. The sibling landed the pinning probe
   (`punctuated-url-cell`: a registry row whose URL cell ends in `.` with the record's `url`
   clean, asserting the bind still succeeds) and this seat re-ran the row at the final bytes
   `c279d952…`: `mutant=url-token-normalization-removal killed=1`, killed by that probe only
   (`exit=1 want=0; missing='MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0';
   missing='records=1 bound=1 unbound=0'`), all other probes pass. Per the mutation-tester
   role: the surviving mutant was a coverage finding, not permission to change the contract —
   the contract was changed by its owner, and the closure is verified.
2. **Inspection-only (not probed — this seat stopped at its assigned probes) — both pinned at
   the final bytes by the sibling:** the malformed-`orphans` exit-2 limb (`orphan_paths` shape
   validation, `capture-binding-check.py:249-266`) is now pinned by the
   `malformed-orphan-declaration` probe (declared orphan without `reason` → exit 2,
   `reason=manifest-shape`), and `parse_round`'s nested first-component split
   (`capture-binding-check.py:88-96`) by the `nested-legacy-round` probe (`round-31/inner` is
   legacy, an archival record passes → exit 0). Still unpinned by construction: the AUDIT
   reporting fields `with_url=`/`with_fetched_utc=`/`with_archival=` (no case asserts them).
   The counter's docstring owns the general limit: "The fixture probes assert the contract
   lines the instrument documents, not every line it prints; a mutant that leaves those lines
   intact while changing other output survives this counter" — disclosed as a bounded oracle,
   so further probe-invisible limbs are limits, not silence.

### 10. No-harm / restoration evidence

- This seat wrote exactly one lane file: this receipt
  (`.ufo/waves/round-34/wave1/MutKillRuleMutants.md`). No lane source, instrument, manifest,
  registry, SCORECARD, lesson or claims file was touched; no `git`/`jj` command was run.
- Instrument bytes before and after all runs:
  `sha256sum corpus/instruments/capture-binding-check.py` →
  `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` at first hash (05:31Z)
  and unchanged at final hash (05:57Z). The counter's digest is re-printed by every run's own
  `KILL-RULE … counter_sha256=` header: `7a20e724…` in §2–§7.
- All mutants were applied to scratch copies (`cbc-live.py` → `mut-*.py`); the pristine scratch
  copy's digest equals the landed digest, so "restored bytes" = the landed bytes themselves,
  never modified by this seat.
- Scratch fixtures lived under `/fast/scratch/hyaku/kasegi-r34/MutKillRuleMutants/` and were
  deleted before this receipt was finalized (`rm -rf` + `test ! -e` → `scratch_removed=1`).
- The counter writes nothing outside its `--scratch` tree; all runs passed
  `--scratch "$S/kr-*"` inside this seat's scratch root.

### 11. Verdict summary for the L1

| probe | expected | observed (frozen bytes `7a20e724…`) | verdict |
|---|---|---|---|
| Counter at tip | `survivors=0`, exit 0 | `survivors=0`, `mutants=3 killed=3`, `gates=6 failed=0`, `controls=4 rejected=4`, exit 0 | **holds** |
| Counter `--selftest` | green | `selftest cases=3 failures=0`, exit 0 | **holds** |
| `skip-selftest-summary` killed | killed | killed=1 by `selftest-shape` alone (summary-only;case-set-mismatch) | **killed** |
| `accept-record-without-url` killed | killed | killed=1 by `selftest-shape` + `record-without-url` fixture | **killed** |
| `per-file-binding-removal` killed | killed | killed=1 by `selftest-shape` + `per-file-orphan` fixture | **killed** |
| Tasked example (url-limb, different wording) reported as survivor | survivor | **killed=1** at every generation — probes are wording-independent | **expectation not met** (counter stronger than tasked) |
| Gen-1 survivor `unnamed-id-guard-removal` | survivor (gen 1) → closed | gen 1: `killed=0`, `survivors=1`, exit 1 (§8); frozen: `killed=1` by `unnamed-record-id` only (§6) | **delivered, then closed** |
| Red-before at the frozen bytes | survivors>0, exit 1 | `url-token-normalization-removal killed=0`, `survivors=1`, `GATE survivors-zero fail`, exit 1 (§7; still survivor at `732e1e31…`, §12) | **confirmed** |
| Coverage gap (url-token normalization limb) | — | probed survivor at gen 3/gen 5 (§7, §12); **CLOSED at the final bytes**: `killed=1` by the new `punctuated-url-cell` probe only (§13) | **finding → closed** |
| Coverage gaps (malformed-orphans exit-2 limb, parse_round nested split) | — | inspection-only (§9.2); **both pinned at the final bytes** by `malformed-orphan-declaration` and `nested-legacy-round` probes (§13 tip run shows all nine pristine probes pass) | **closed by owner** |

Caveat for integration: §2–§8's figures are generation-pinned (counter `7a20e724…`, instrument
`3d9e5e0d…`); §12 re-confirms at `732e1e31…`; §13 re-confirms at the FINAL bytes
`c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` (43138 B, 881 lines), where
the sibling declares no further edits. The three C1-load-bearing verdicts — tip `survivors=0`
exit 0, the three named mutants `killed=1`, and a surviving row printing `survivors=1` exit 1 —
held at every generation this seat measured (gen 1, gen 3, gen 5, final). The gen-1 history
(§8) is generation-pinned and needs no re-run.

### 12. Re-confirmation at the latest observed bytes (`732e1e31…`)

While this receipt was being finalized the counter moved twice more (`b8e4fb4c…`, then
`732e1e31…`; the sibling executor is still iterating — the new `named-rows` gate appears, the
probe set stays at six). Both load-bearing verdicts were re-run at `732e1e31…`:

```
python3 corpus/instruments/kill-rule-check.py --scratch "$S/kr-tip3" | grep -E '^(KILL-RULE|probe |pristine|mutant=|controls=|GATE|mutants=|gates=|survivors=)'; echo "tip3_exit=${PIPESTATUS[0]}"
```

```
KILL-RULE instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa bytes=40556 lines=892 floor=19 counter_sha256=732e1e319298295709b3917fb0a9753192c0af455d912543deac82c513c88708
probe selftest-shape pristine=pass exit=0
probe record-without-url pristine=pass exit=1
probe per-file-orphan pristine=pass exit=1
probe unnamed-record-id pristine=pass exit=1
probe stale-orphan-declaration pristine=pass exit=1
probe malformed-fetched-utc pristine=pass exit=1
pristine selftest cases=23 case-lines=23 floor=19 floor_met=1
mutant=skip-selftest-summary killed=1
mutant=accept-record-without-url killed=1
mutant=per-file-binding-removal killed=1
controls=4 rejected=4
GATE ok name=named-rows
GATE ok name=pristine-selftest
GATE ok name=pristine-fixtures
GATE ok name=pristine-determinism
GATE ok name=rows-valid
GATE ok name=controls
GATE ok name=survivors-zero
mutants=3 killed=3 survivors=0 invalid=0
gates=7 failed=0
survivors=0
tip3_exit=0
```

```
python3 corpus/instruments/kill-rule-check.py --scratch "$S/kr-runC3" --row-file "$S/r6.json" | grep -E '^(KILL-RULE|mutant-patch name=url-token|mutant-bytes name=url-token|mutant-probe name=url-token|mutant=url-token|GATE fail|GATE ok name=survivors|mutants=|gates=|survivors=)'; echo "runC3_exit=${PIPESTATUS[0]}"
```

```
KILL-RULE … counter_sha256=732e1e319298295709b3917fb0a9753192c0af455d912543deac82c513c88708
mutant-patch name=url-token-normalization-removal patch_sha256=1f72a07707bd0245 find_sha256=0dc5098846fd7602 find_count=1 status=ok
mutant-bytes name=url-token-normalization-removal pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=2e1ba326bd1a9d90
mutant-probe name=url-token-normalization-removal probe=selftest-shape pristine=pass mutant=pass exit=0
mutant-probe name=url-token-normalization-removal probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant=url-token-normalization-removal killed=0
GATE fail name=survivors-zero
mutants=4 killed=3 survivors=1 invalid=0
gates=7 failed=1
survivors=1
runC3_exit=1
```

Both verdicts hold at the latest observed bytes: the tip command prints `survivors=0` exit 0
(now under seven gates), and the §7 survivor probe still reports
`url-token-normalization-removal killed=0` → `survivors=1`, exit 1 — the normalization limb
remains unpinned at `732e1e31…`.

Post-§12 observation (recorded, not re-measured): one more counter generation appeared while
this receipt's final hashes were taken — `sha256sum corpus/instruments/kill-rule-check.py` →
`8d12d45f90f7a30584188f3db48c8eccab3047901e9b92b023bd7e9a3ce92308` (06:00Z window). The
sibling executor is still iterating; every verdict in this receipt is generation-pinned by its
own `counter_sha256=` header, and the three verdicts that matter for C1 (tip `survivors=0`
exit 0; the three named mutants `killed=1`; the counter reports a surviving row as
`survivors=1` exit 1) held at every generation this seat measured (gen 1, gen 3, gen 5).

### 13. Final-bytes confirmation (`c279d952…`) — the open finding is closed

The sibling declared the final counter bytes
`c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` (43138 B, 881 lines; "no
edits by me after this message") with the probe set grown to eight fixtures + the shape gate —
including a `punctuated-url-cell` probe of exactly the shape §9.1 named, plus
`malformed-orphan-declaration` and `nested-legacy-round` for §9.2's inspection-only limbs.
This seat re-hashed (`c279d952…` confirmed on disk) and re-ran both load-bearing commands:

```
python3 corpus/instruments/kill-rule-check.py --scratch "$S/kr-final" | grep -E '^(KILL-RULE|probe |pristine|mutant=|controls=|GATE|mutants=|gates=|survivors=)'; echo "final_tip_exit=${PIPESTATUS[0]}"
```

```
KILL-RULE instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa bytes=40556 lines=892 floor=19 counter_sha256=c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61
probe selftest-shape pristine=pass exit=0
probe record-without-url pristine=pass exit=1
probe per-file-orphan pristine=pass exit=1
probe unnamed-record-id pristine=pass exit=1
probe stale-orphan-declaration pristine=pass exit=1
probe malformed-fetched-utc pristine=pass exit=1
probe punctuated-url-cell pristine=pass exit=0
probe malformed-orphan-declaration pristine=pass exit=2
probe nested-legacy-round pristine=pass exit=0
pristine selftest cases=23 case-lines=23 floor=19 floor_met=1
mutant=skip-selftest-summary killed=1
mutant=accept-record-without-url killed=1
mutant=per-file-binding-removal killed=1
controls=4 rejected=4
GATE ok name=named-rows
GATE ok name=pristine-selftest
GATE ok name=pristine-fixtures
GATE ok name=pristine-determinism
GATE ok name=rows-valid
GATE ok name=controls
GATE ok name=survivors-zero
mutants=3 killed=3 survivors=0 invalid=0
gates=7 failed=0
survivors=0
final_tip_exit=0
```

```
python3 corpus/instruments/kill-rule-check.py --scratch "$S/kr-m6final" --row-file "$S/r6.json" | grep -E '^(KILL-RULE|mutant-patch name=url-token|mutant-bytes name=url-token|mutant-probe name=url-token|mutant=url-token|GATE|mutants=|gates=|survivors=)'; echo "m6_final_exit=${PIPESTATUS[0]}"
```

```
KILL-RULE … counter_sha256=c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61
mutant-patch name=url-token-normalization-removal patch_sha256=1f72a07707bd0245 find_sha256=0dc5098846fd7602 find_count=1 status=ok
mutant-bytes name=url-token-normalization-removal pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=2e1ba326bd1a9d90
mutant-probe name=url-token-normalization-removal probe=selftest-shape pristine=pass mutant=pass exit=0
mutant-probe name=url-token-normalization-removal probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=url-token-normalization-removal probe=punctuated-url-cell pristine=pass mutant=fail exit=1 reasons=exit=1 want=0;missing='MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0';missing='records=1 bound=1 unbound=0'
mutant-probe name=url-token-normalization-removal probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=url-token-normalization-removal probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=url-token-normalization-removal killed=1
GATE ok name=named-rows
GATE ok name=pristine-selftest
GATE ok name=pristine-fixtures
GATE ok name=pristine-determinism
GATE ok name=rows-valid
GATE ok name=controls
GATE ok name=survivors-zero
mutants=4 killed=4 survivors=0 invalid=0
gates=7 failed=0
survivors=0
m6_final_exit=0
```

At the final bytes: the tip command prints `survivors=0` exit 0 with all nine pristine probes
passing; the §7 survivor row is now `killed=1`, killed by the `punctuated-url-cell` probe and
by that probe only (`selftest-shape` shows `mutant=pass`) — the pristine bytes bind a
punctuated-URL cell's clean record (`exit=0`, `url_bound=1`) and the mutant fails to bind.
The red-before obligation remains demonstrated by this receipt's generation history (§8 gen-1
survivor → closed; §7/§12 survivor → closed at the final bytes) and by the counter's own
`CTL-equivalent` witness on every run; the sibling's receipt §7 additionally records its
deliberate comment-only red row (`attack-comment-only killed=0`, `survivors=1`, exit 1).

Report: .ufo/waves/round-34/wave1/MutKillRuleMutants.md
