# RevSourceRecheck — receipt (round 36, wave 1, coverage)

Seat: RevSourceRecheck (reviewer, leaf). Item: verify the F19 entry's recheck command line per QUALITY Q10 (one executable command, `bash -n` parseable, carries `cd {LANE} &&`, `--manifest corpus/source-snapshots/round-36/manifest.json --source S053`, human note after `#`), and verify fail-closed exit 2 on a missing capture. Tooling installs: none.

## Target line (verbatim, from ScribeEntryF19 via peer message, 2026-10-26)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053   # prints S053:sha256 OK then one S053:Q<n> OK line per pinned quote with occurrences=1 and anchor=N-ok; exits 2 when the manifest or capture is absent and 1 when the sha256 differs or a quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check
```

The knowledge entry `corpus/knowledge/epss-exploit-prediction-scoring.md` is not yet landed at the frozen head b47f2cdf (working tree and `git archive HEAD` export both lack it, and lack `corpus/source-snapshots/round-36/`); the line above is the scribe's draft text, byte-checked below. L1 lands it unchanged.

## Findings — all five item criteria PASS

1. **One executable command** — PASS. Byte checks on the verbatim line (scratch, `python3` structural pass): single logical line (no embedded newline); the only `&&` joins `cd <lane-root>` to the one `python3` invocation; no `;`, `|`, or `&` outside the `#` comment. Not a prose sentence with a command appended (Q10's rejection class).
2. **`bash -n` parseable** — PASS. `bash -n` on the file holding the verbatim line: rc=0 (scratch `G`). Also rc=0 for the literal `cd {LANE} && …` template form.
3. **`cd {LANE} &&` prefix** — PASS. Command portion starts exactly `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && `, matching Q10 "carries its own `cd <lane-root> &&` prefix so it runs from any cwd".
4. **`--manifest corpus/source-snapshots/round-36/manifest.json --source S053`** — PASS. Both argument pairs present verbatim in the command portion.
5. **Human note after `#`** — PASS. Note follows the first unquoted `#` (two spaces before it), is prose describing expected output and failure semantics (`…; a pinned-capture comparison, not a fresh network check`), and does not alter the command.

## Fail-closed on missing capture → exit 2 — PASS (independently reproduced three ways)

Run from a foreign cwd (`/`), instrument bytes proven identical to the lane (`sha256 fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` for both the `git archive HEAD` export copy and the working-tree copy):

- **Verbatim line, live, pre-landing**: rc=2, output `manifest UNAVAILABLE reason=missing` — the round-36 manifest is not landed yet, and absence of the base fails closed rather than passing silently (this rc=2 is the correct pre-landing reading; it is not a pass of the entry's content).
- **Manifest present, capture deleted**: `git archive HEAD` export with `round-35/manifest.json` filtered to S052 and `S052.txt` deleted → rc=2, `S052:source UNAVAILABLE reason=missing`.
- **Instrument source** (`corpus/instruments/source-recheck.py`): `load_manifest` catches `FileNotFoundError` → `reason=missing`, returns 2; `check_source` catches capture `FileNotFoundError` → `reason=missing`, returns 2; `recheck` propagates 2 over 1. An absent manifest, an unlisted `--source`, or an absent capture all exit 2.

**Contrast (semantics are honest, not always-2)**: tampered capture bytes → rc=1 (`S052:sha256 MISMATCH expected=d69349e8… actual=92e78d0b…`); tracked round-35 positive control `--manifest corpus/source-snapshots/round-35/manifest.json --source S052` from `/` → rc=0 with five `OK occurrences=1 anchor=N-ok` lines, proving the `cd` prefix genuinely resolves from any cwd and the happy path is reachable.

## Residual risk / verification gaps

- Post-landing rc=0 (`S053:sha256 OK`, Q1..Q4 `anchor=216-ok/217-ok/217-ok/235-ok`) is **unverified by this seat** — `corpus/source-snapshots/round-36/{S053.txt,manifest.json}` do not exist at the frozen head; landing them is the L1 integration step. Anchor correctness is the instrument's own post-landing check (Q3/Q9 lane), not this item.
- The line was verified from the scribe's peer message; if the landed entry's line differs by even one byte, re-run `bash -n` + the structural checks on the landed bytes (commands above are one-line reproducible).

Scratch dir `/fast/scratch/hyaku/kasegi-r36/RevSourceRecheck/` removed before yield. No lane, fleet, or source-tree files were modified; only read-only git was used.
