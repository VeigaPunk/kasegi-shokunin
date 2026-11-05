# Round-78 C1 mutant transform table (frozen with the claims)

Each mutant is derived from the LANDING successor bytes (the counter at the round-78 landing
commit) by exactly ONE anchored text transform below. The successor keeps the r77 reference's
selftest structure (`.ufo/waves/round-77/c1-amended-reference.py`, sha256 `18bfc439238310af345189c0192c497b8451bea4a2bed1644a03866924588a33`,
anchors cited by its line numbers) plus the R-77-A TMPDIR refusal. A transform whose anchor is
absent from the landing bytes is recorded NOT DERIVED and counts as NOT VERIFIED (claims.json kill rule).

| id | anchor in landing bytes (exact text) | transform | expected verdict | kill class |
|---|---|---|---|---|
| K-M1 | the two-line statement beginning `regs["restoration-only-result"] = lambda out, ret: (` | delete the statement through `ret == 1 and "RECHECK-CWD-RESULT nonconformant" in out)` | selftest exits 1; `gate-regs FAIL`; `gate-consume FAIL no-registration`; FAIL lines, no traceback | assertion |
| K-M2 | the registration closure body `(ret == 1 and "RECHECK-CWD-RESULT nonconformant" in out)` | replace the body with `True` (arguments unconsumed) | selftest exits 1; `gate-consume ok clean_ok=True`; `gate-negpolarity FAIL neg_ok=True` | assertion (required m2b-class kill) |
| K-M3 | the case-6 line `out6, ret6 = capture(main, ["recheck-cwd-census.py", "--root", root6, "--lane", root6])` | delete the line | selftest exits 1; `gate-consume FAIL exception=NameError(...)` | exception (logged distinctly; not a kill of the consumed assertion) |
| K-M4 | `check("gate-negpolarity", neg_ok is False, "neg_ok=%r" % (neg_ok,))` | `neg_ok is False` -> `neg_ok is True` | selftest exits 1; `gate-negpolarity FAIL neg_ok=False` | assertion |
| K-M5 | the whole `check("both-headers", ...)` call (its four lines; fixture setup kept) | delete the call | selftest exits 1; `gate-checkids FAIL missing=['both-headers']` | assertion |
| K-X1 | `clean_ok = limb(out6, ret6)` (reference line 318) | replace with `clean_ok = True` (consumer neutered; r77 survivor X1) | selftest exits 1 by an assertion FAIL on the case-6 limb or gate-consume | assertion (required) |
| K-X2 | `check("gate-consume", clean_ok is True, "clean_ok=%r" % (clean_ok,))` (reference line 323) | replace the condition `clean_ok is True` with `True` (gate-consume body neutered; r77 survivor X2) | selftest exits 1 by an assertion FAIL on a case-6 polarity check | assertion (required) |
| K-M8 | the first argument pair of `check("relabel-detection", <expr>, ...)` (reference line 305) | replace `<expr>` with `True` (relabel-detection body neutered; r77 survivor K-M8) | selftest exits 1 by an assertion FAIL in relabel-detection or gate-checkids | assertion (required) |

Known limits (routed, not frozen kills): composite mutants combining two named transforms, and
the gate-negpolarity boolean inside a second closure, are outside the named kill set; a survivor
there is routed to the next round, not a claim failure.

Red-before evidence (committed, not re-derived by this table): the r77 reference's receipts show
X1, X2 and K-M8 survive (`selftest cases=12 failures=0`, rc0) in
`.ufo/waves/round-77/w1/RevengerInherited-run-X1-consumer-const.txt`,
`.ufo/waves/round-77/w1/RevengerInherited-run-X2-gateconsume-bool.txt` and `.ufo/waves/round-77/w1/MutC1.md`.
