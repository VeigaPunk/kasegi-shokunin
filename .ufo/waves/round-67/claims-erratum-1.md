# Round-67 claims erratum 1 — collector sub-assertion and a digest transcription error

Filed 2026-11-04 by the L1 (KasegiR67), after the first `--final` run at controls revision
`7ae95a0662adefff9bca5fed3075d3671a9e000d`. Both receipts are kept; the frozen predicate, the
probe set, the pins' content, the MEASUREMENTS tuple and every verdict rule are unchanged.

## E1 — the multihead-mutbat measurement failed on a diagnostic line, not on a verdict

First final run:

```
RESULT multihead-mutbat FAIL exit=0 want='MUTBAT killed=7/7 survivors=0 equivalents=3 invalid_rejected=0 failures=0'
  sha256=88e0c3e6… collector-ignored-FAIL COLLECTOR fixtures=ok root=…/collector-root
VERIFY measurements=12 failures=1 revision=b30820609b03 mode=final
```

The battery DID consume the shared collector: its receipt prints
`probes=collector:d56a1437…(probe_table) count=33 builtin=14 collector=19`, then
`COLLECTOR fixtures=ok` and `COLLECTOR unstable=P10`. The driver's assertion treated ANY
`COLLECTOR ` line as "collector ignored", so the collector's own legitimate finding (P10's
native face is flaky — the fact this round measured and froze) was scored as a harness failure.
The claim's verdicts in that run were all green: `probes-measured PASS` (all five repair shapes
stale with `derive-upstream-signal-13` on every observed face), `shape-identity PASS` (20 shapes),
`selftest PASS 73/0`, `mutbat-existing PASS 5/5`, `real-ledger PASS 35/35`, `red-wrong-want PASS`,
`identity-guards PASS`. Only the diagnostic-line assertion failed.

Bounded fix (this erratum): the measurement now fails only on a literal `COLLECTOR ignored=` line
or a missing `probes=collector:` binding line, and records other `COLLECTOR …` lines as
`collector-findings=…` in its note. The battery bytes, the gate bytes, the probe bytes, the pins'
content and every expectation string are unchanged; the driver digest changes
`61d5a048…` → the erratum digest recorded in `controls/driver-pins.json`.

Preserved receipts: `controls/erratum1-collector-first-receipt.txt` (the failing run's own
multihead-mutbat receipt). The failing run's full stdout was not captured to a file before the
fix; the driver line quoted above is the whole of its evidence for that measurement, and the
re-run's receipt is the measured record. This is a process miss (M67-9): the first final run
should have been tee'd to a file like every other round's.

## E2 — claims.json records the wrong battery digest

`claims.json` (frozen at `b30820609b03`) names `mutbat_sha256`
`e6d54540da721ff2622da32249e0898d411ee832607d677c387508717467b9d2` for
`.ufo/waves/round-67/w1/MutationMultiHead/multihead-mutbat.py`. The bytes committed at the
controls revision and pinned in `controls/driver-pins.json` are
`88e0c3e63ab951b208bbceebcf4eae749e58b8a5dc96cf379e3e73227716761b`: the mutation seat superseded
its battery between the L1's digest read and the pin refresh, and the L1 transcribed the earlier
value into the frozen record. The pin, the commit and the measurement all agree on `88e0c3e6…`;
only the claims cell is wrong. It is corrected here, not rewritten in the frozen file.

A second, post-freeze edit of the same battery (`cf42921b…`, a face-tolerant DIFFERENTIAL row) was
found in the worktree after the commit; the L1 reverted the worktree to the committed bytes and
records the post-commit control edit as M67-10. The newer bytes are not measured and are not
carried by this round.

## E3 — the counting command's controls revision

The frozen `counting_command` names `--controls-revision 7ae95a06…`. The re-run uses the erratum
commit as `--controls-revision` (it carries the same gate, probes, battery and pins content plus
this erratum and the corrected pins). The measured gate bytes are identical in both
(`8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247`).
