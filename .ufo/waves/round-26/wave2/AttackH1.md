# Attack H1 — live audit receipt regeneration

- **Attack:** Re-run the live `recheck-audit.py` command against the landed lane and check the generated result against the L1-owned `.ufo/waves/round-26/c1-live.json` without overwriting it.
- **Command:** `python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-26/wave2/h1-live-regen.json` (from the lane root).
- **Observed exit:** `0`.
- **Observed summary:** `lines=39 total=39 pass=39 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`; `expect=present expected=39 missing=0 unexpected=0 exit=0`. Strict summary: `pass=39/39 cdroot_fail=0 instrument_fail=0 own_fail=0`. The instrument digest recorded in generated JSON is `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`.
- **Receipt comparison:** Generated JSON at `.ufo/waves/round-26/wave2/h1-live-regen.json` compared byte-for-byte identical (`cmp` success) to `.ufo/waves/round-26/c1-live.json`. Both SHA-256 values observed as `b3d1750e57b8188cbf3bcdfa25bc7f2e3d201e69a91884e32db30c7f0c20be99`. The L1-owned receipt was not modified.
- **Deviation:** None from the expected summary; expected-list check was present and complete.
