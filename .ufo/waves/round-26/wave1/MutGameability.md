# Round 26 counter gameability probes

Date: 2026-10-25 UTC. Scope: frozen C1/C2 counter commands in `.ufo/waves/round-26/claims.json`; scratch-only probes. No production edits.

| Probe | Observed scratch output | Would frozen counter catch it? |
|---|---|---|
| C1: fabricate `selftest cases=15 failures=0` without running selftest | Wrote literal line to scratch receipt; `grep -cE 'selftest cases='` returned `1`; receipt size 29 bytes. | **No.** The AFTER receipt-line count is met without any selftest execution or digest binding. |
| C1: point `--expect` at empty file so missing entries become `[]` | Inspected live `recheck-audit.py`; there is no `--expect` argument or expected-list behavior. Current `knowledge-expected.txt` has 39 lines. | **Not a supported bypass** for the instrument present. Could not reproduce as described; no claim that an alternate control implementation behaves this way. |
| C2: F11 admitted while a new entry is an empty shell citing S041 | Scratch shell with only `source: S041 https://example.invalid exact anchor` produced frozen citation grep count `1`; a skeletal F11 admitted row produced awk count `1`. | **No**, for those counters: neither verifies substance/quality. Frozen census and kill rule add separate constraints, but census was not run on the intentionally incomplete scratch fixture, so its result is unknown. |

C2 counter qualification: the citation pattern `^source: S04[0-9]` includes S040; the committed do-nothing control records a baseline count of 1 from the round-25 S040 citation. Thus the frozen grep alone neither isolates S041 nor proves the row is cited by a substantive admitted entry. The frozen claim's explicit census-exit and every-new-row-cited kill rule remain separate requirements, not findings that the probes validated.

Exact probe notes: `.ufo/waves/round-26/c1-controls/m3-gameability.txt` and `.ufo/waves/round-26/c2-controls/m3-gameability.txt`. Scratch probe directory: `/tmp/kasegi-m3-game.8GlaaR`. No tools installed.