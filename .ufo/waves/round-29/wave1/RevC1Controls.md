# RevC1Controls — round 29 wave 1

## Findings

No actionable findings.

## Verified

- **Do-nothing control:** `c1-controls/before.txt` and its three split receipts record base digest `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`, cases=9, zero limb-coverage matches, and git-free exit 1/`FileNotFoundError`. The base digest matches the frozen claim. The control cannot meet the target.
- **Production target:** the live `anchorcheck.py` SHA-256 is `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`, matching `c1-receipt-index.txt:3`; that receipt's 561-line count matches. I independently replayed all three frozen C1 counter forms: 12 cases, 0 failures, limbs=9 covered=9; grep emits both lines; git-free run prints `SKIP pin-broken (git not found)` and exits 0. The commands parse and emit the target values (M28-3 class checked).
- **Receipts:** baseline digest and observed values agree with the frozen base bytes. Canonical receipt digest is pinned to the current production bytes. Its SKILL no-harm output records 7 in-range, 0 bad, LOST-RECORDED=306, exit 0.
- **M1:** my run of `/tmp/mutant-m1.py --selftest` returned exit 1 with missing `outside-base-mirror`, cases=11, failures=1, covered=8. Receipt agrees.
- **M2/M3:** both mutations were detected by the frozen output assertion (`frozen_assertion_exit=1` in their receipts), and I reproduced that their *instrument* selftest process itself exits 0: M2 omits the `limbs=` line; M3 prints covered=8. The distinction should remain explicit: the fixed selftest's internal return code alone does not fail on either output-only mutation, while the frozen counter assertion does.
- **M4:** verified the isolated mutation in `mutant-m4.txt` and independently reran it. Only the `GIT_*` filtering changes to `dict(os.environ)`; git-presence guard and case logic remain. Under `GIT_OBJECT_DIRECTORY=/dev/null`, the mutant fails `git init`, skips the pin limb, and exits 1 (`covered=8`); the fixed bytes under the identical poison exit 0 with 9/9 coverage.

## Residual risk / verification gap

M2/M3 require the frozen output assertion to detect their missing/incorrect printed counters; the selftest's own return code remains 0 for these output-only mutations. No other check gaps observed.
