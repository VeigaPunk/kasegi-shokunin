# Round-77 C1 mutant transform table (frozen with the claims)

Each mutant is derived from the frozen reference implementation
`.ufo/waves/round-77/c1-amended-reference.py` (sha256 `18bfc439238310af345189c0192c497b8451bea4a2bed1644a03866924588a33`)
by exactly ONE of the transforms below. A seat may rebuild them independently; a rebuilt
mutant must be byte-identical to the committed controls copy after applying the same
transform, or its derivation names its own diff.

| id | transform (exact) | expected verdict | kill class |
|---|---|---|---|
| K-M1 | delete the two-line registration statement beginning `regs["restoration-only-result"] = lambda out, ret: (` through `ret == 1 and "RECHECK-CWD-RESULT nonconformant" in out)` | selftest exits 1; `gate-regs FAIL` plus `gate-consume FAIL no-registration` / `gate-negpolarity FAIL no-registration`; FAIL lines, no traceback | assertion |
| K-M2 | replace the registration closure body `(ret == 1 and "RECHECK-CWD-RESULT nonconformant" in out)` with `True` (arguments unconsumed) | selftest exits 1; `gate-consume ok clean_ok=True`; `gate-negpolarity FAIL neg_ok=True` | assertion (THE required m2b-class kill) |
| K-M3 | delete the case-6 line `out6, ret6 = capture(main, ["recheck-cwd-census.py", "--root", root6, "--lane", root6])` | selftest exits 1; `gate-consume FAIL exception=NameError(...)` and `gate-negpolarity FAIL not-evaluated-after-exception` | exception (logged distinctly; not a semantic kill — R127) |
| K-M4 | in the gate-negpolarity check, change `neg_ok is False` to `neg_ok is True` | selftest exits 1; `gate-consume ok clean_ok=True`; `gate-negpolarity FAIL neg_ok=False` (the intact closure returns False on the case-2 conformant outputs) | assertion |
| K-M5 | delete the whole `check("both-headers", ...)` call (four lines, fixture setup kept) | selftest exits 1; `gate-checkids FAIL missing=['both-headers'] extra=[]`; printed `cases=11 failures=1` | assertion |

Committed derivations (controls/, sha256 at freeze): m1 `c2746492…`, m2 `b7772949…`,
m3 `1fd8d29a…`, m4 `7f5bb936…`, m5 `b7af7722…`. The base counter
(`corpus/instruments/recheck-cwd-census.py`, sha256 `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a`)
is untouched by all five transforms — it has no gate to kill; the red-before evidence for the
survivor class is the committed round-76 receipt re-run at
`controls/c1-redbefore-r76-survivor-r77.txt` (the r76 candidate design's
`m2b-conjunct-removed.py --selftest` → `selftest cases=8 failures=0`, rc 0).

Known limits (routed, not frozen kills): a mutant that neuters the gate-negpolarity check's
own boolean (`neg_ok is False` → `True`) while leaving the closures intact, or composite
mutants combining two named transforms, are outside the named kill classes; a survivor in
those classes is routed to the next round, not a claim failure.
