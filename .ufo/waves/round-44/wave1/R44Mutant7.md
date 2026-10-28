# R44Mutant7 — exit-code conflation probe

## Finding

The claimed distinction is real at the command boundary: `ls /no/such/kasegi-suite.sh` printed `ls: cannot access ...` and returned **2**, while `bash /no/such/kasegi-suite.sh` printed `bash: ... No such file or directory` and returned **127** (both direct probes run from scratch). The committed round-43 control reproduces the first case at `.ufo/waves/round-43/c1-controls/do-nothing.txt:4-5` (`ls` then `exit=2`); its later line 41 quotes `exit 127` as a round-42 claim, not as output of the cited `ls`.

The frozen round-43 C1 `before` cell at `.ufo/waves/round-43/claims.json:38` says “the r43 suite is absent at base (exit 127)” while citing that control. Thus the defect is a citation/measurement mismatch; the number 127 can be a valid result of direct execution of an absent script, but it is not the measured result printed by the cited `ls` probe.

## Existing-detector result / do-nothing discrimination

Ran committed K17 against six isolated fixtures built from the committed C1/control bytes: original claim, claim changed to exit 2, genuine appended direct-execution exit 127, false-conflation erratum, exit=12 prefix trap, and honest erratum. All six returned the identical output:

`K17 payload=claims=1,tokens=2,verified=2,superseded=0,unbacked=0,quoted=2 closed=1` (rc 0).

This is an observed blind spot, not a K17 failure: `k17-claims-before.sh:105` defines `TOKEN_RX` as only `closed|failures|cases`; it never extracts `exit=`/`exit ` tokens. K18 likewise uses `SUM_CLOSED_LINE` and `EXIT_AFTER` only to bind/shape `closed=` summaries (`k18-transcript.sh:71,181,191`); it does not compare an exit code in a claim with its cited receipt. These gate files are byte-identical between frozen round-44 base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` and inspected HEAD (`git diff --stat <base> HEAD -- ...` was empty). The round-44 frozen do-nothing control says no r44 counter existed at freeze. Therefore do-nothing and this committed claims/control gate cannot distinguish the defect from a correction; no committed exit-token detector was found in the inspected tree.

A naïve whole-token presence match is also unsound: the cited control's line 41 contains “exit 127” inside a quotation about the round-42 control. The measurement is line 5 `exit=2`; treating any text occurrence as measurement would accept the false 127.

## Mutant and bounded detector

Scratch-only D_min probe: compare whole `exit <n>` / `exit=<n>` tokens in `before` cells against exit values on machine-shaped receipt lines (`exit=<n>` or key/value output ending in `exit=<n>`). It excludes quoted prose. An erratum escape is accepted only when it names the superseded token and supplies a different measured value printed by the cited receipt. This is a probe design, not a committed gate; it borrows K18's summary-shaped-versus-prose distinction and is limited to this assigned exit-code attack.

Fixtures: F0 = committed round-43 C1/control (127 claim, measured 2); F1 = same claim with 2; F2 = same control plus a directly executed missing script yielding measured 127; F3 = F0 plus a false erratum saying the cited control prints 127; F4 = F0 with measured exit 12 instead of 2; F5 = F0 plus an honest erratum naming measured 2. Bounded battery expectations: reject F0/F3/F4; accept F1/F2/F5.

- **M7 (named conflation):** one-line backing mutant `backed = val in printed` → `backed = bool(printed)`, so any nonzero measured control exit (including 2) backs a claim of 127. Detector output on M7: F0/F3/F4 incorrectly accepted; full battery `cases=6 failures=3` (rc 3). **Killed** by F0. Pristine full battery: `cases=6 failures=0` (rc 0).
- **M8 (erratum-path conflation):** one-line escape mutant `if any(x in printed for x in other):` → `if True:`. It lets an erratum that only repeats the unsupported 127 stand in for a measured correction. Reduced F0/F1/F2 battery: `cases=3 failures=0` (rc 0), so **survives** that common minimal set. Full battery rejects it only on F3: `cases=6 failures=1` (rc 1), so **killed** when the false-erratum fixture is included. This is the coverage finding: an exit=2-vs-127 test alone does not exercise the erratum escape.

Other exact observed probe outputs: pristine D_min — F0 reject (`tokens=2,backed=1,superseded=0,unbacked=1`), F1 accept (`2,2,0,0`), F2 accept (`2,2,0,0`), F3 reject (`2,1,0,1`), F4 reject (`2,1,0,1`), F5 accept (`2,1,1,0`). On the live claims pair with both cited round-43 controls included, D_min returned `tokens=3,backed=2,superseded=0,unbacked=1 closed=0`, specifically `unbacked token=exit=127`; committed K17 returned `...closed=1` (rc 0). This is probe evidence only, not a lane counter verdict.

## Hashes and restoration

Scratch detector pristine SHA-256: `5a449dccde09995dec43c3ce93c89a076aaf204a67792b11891f9f38e672c272`.

- M7 mutated copy SHA-256: `0e8cad772b90a3753981e0463cac4c0f51a160bf1bc65eb0fa02f2f0c7611fdf`; restored copy SHA-256 returned to pristine `5a449d…`; restored full battery again `cases=6 failures=0`.
- M8 mutated copy SHA-256: `b688e2308831f5955a36dc186abc4efd87881123a87c208445768e77baf171f8`; restored copy SHA-256 returned to pristine `5a449d…`; restored full battery again `cases=6 failures=0`.

All fixtures, detector copies, and outputs were under `/fast/scratch/hyaku/kasegi-r44/R44Mutant7/`; `HYAKU_SCRATCH` was unset, so `/fast/scratch/hyaku` was used as the local scratch root. No tool was installed. Scratch cleanup is performed before exit.

## Limitations

D_min and its fixtures were scratch-designed for this single attack; neither is a round-44 committed detector, so this does not establish that C1's final counter catches or fails the defect. The report does not claim an implementation correction or final-round verdict. The measured-line grammar is intentionally bounded to machine-shaped transcript lines; a production gate must preserve the lane's existing receipt formats and avoid treating quoted/payload text as measurements.
