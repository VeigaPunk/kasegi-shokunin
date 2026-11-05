# SentinelC1 — security review of the C1 amended counter candidate (diff only)

Round 76, wave 1, attempt 1. Seat: SentinelC1 (sentinel, leaf — no subagent dispatch).
Scope per seat spec: the six surface checks against the amendment diff only; no claim
verdicts (A1–A5 adjudication is not mine).

## VERDICT: NO-REVIEW — TARGET ABSENT (recorded and stopped per seat spec)

The seat spec mandates: "Wait once for `.ufo/waves/round-76/w1/ExecC1Amend.patch` (if
absent after your setup steps, record that and stop)."

- Setup steps completed first: claims.json read in full; scratch created;
  frozen base counter fetched read-only from git.
- One wait exercised: a single bounded poll, 5 s interval × 48 = 240.08 s wall
  (command: `while [ $i -lt 48 ]; do [ -f "$W/ExecC1Amend.patch" ] || [ -f "$W/ExecC1Amend.amended.py" ] && break; sleep 5; done`,
  rc=0), run 2026-11-05 ~07:54–07:58 local.
- Outcome: `ExecC1Amend.patch` ABSENT and `ExecC1Amend.amended.py` ABSENT at end of
  window (`ls` rc=0; dir listing retained in the poll output). The wave dir did gain
  `ExecC1Controls-step{1,2}-*.txt` during the same window, so executor siblings were
  writing — the amend artifacts specifically never landed.

This is NOT a 'CLEAN' verdict: no diff existed to review, so no security claim about the
amendment is made here. Checks (1)–(6) below are UNRUN against the amendment; the
baseline they must be diffed against is grounded below.

## Grounded baseline (frozen base counter, for whoever re-runs the review)

Base bytes fetched: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e:corpus/instruments/recheck-cwd-census.py`
rc=0, 281 lines.
- `sha256sum` → `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a` rc=0 —
  matches the claims.json C1 pin byte-for-byte.

Before-state surface counts (run on that verified copy; exit codes as reported):
| # | check | command | count | rc |
|---|-------|---------|-------|----|
| 1a | bash -c pair | `grep -c '\["bash", "-c"'` | 1 | 0 |
| 1b | subprocess.run sites | `grep -c 'subprocess\.run'` | 1 | 0 |
| 1c | Popen/os.system/shell=True | `grep -cE 'Popen\|os\.system\|shell=True'` | 0 | 1 (no match = pass) |
| 3 | network imports | `grep -cE 'import (socket\|urllib\|requests\|http)\|from (socket\|urllib\|requests\|http)'` | 0 | 1 (no match = pass) |
| 2 | open() sites | `grep -n 'open('` | 3 | 0 |
| 6 | /tmp literals | `grep -c '/tmp'` | 1 | 0 |
| — | mkdtemp sites | `grep -c mkdtemp` | 8 | 0 |
| 4 | sysctl/pacman/systemctl/service | `grep -cE 'sysctl\|pacman\|systemctl\|service '` | 0 | 1 (no match = pass) |
| 4 | os.environ sites | `grep -n 'os\.environ'` | 4 | 0 |

Before-state interpretation (base bytes, line numbers from that copy):
- The one bash -c site is `run_foreign` L68: `subprocess.run(["bash", "-c", value], cwd=scratch, env=env, stdin=DEVNULL, capture_output=True, text=True, timeout=120)` — no shell=True anywhere.
- open() sites: L47 and L56 are read-only knowledge-file reads; L135 is the selftest
  `write_entry` writing `"w"` into `os.path.join(kdir, name)` where `kdir` is under the
  `tempfile.mkdtemp(prefix="recheck-cwd-selftest-", dir=os.environ.get("TMPDIR") or None)` scratch (L132). No fixed-path write exists.
- Cleanup: `shutil.rmtree(..., ignore_errors=True)` in `finally` at L77 (run_foreign) and L251 (selftest).
- The single `/tmp` literal is L25 docstring prose ("no path is hard-coded under /tmp") — not a path use.
- os.environ sites: L67 `dict(os.environ)` is env passthrough to the child bash (pre-existing, by design — the recheck value runs with the caller's environment); L84/L132/L208 are TMPDIR reads only. No other env harvesting.

## Re-run recipe (checks 1–6, unrun against the amendment)

When `ExecC1Amend.patch` / `ExecC1Amend.amended.py` lands, run the same greps on the
amended FULL file (not just hunks), plus a hunk-level review:
1. exec surface: counts for `["bash", "-c"` must stay exactly 1, `subprocess.run` exactly 1, `Popen|os.system|shell=True` 0. FAIL if the amendment adds any exec call site.
2. write surface: enumerate every `open(` — no `"w"`/`"a"`/`"x"` mode on a path that is not under a `tempfile.mkdtemp(dir=TMPDIR-or-None)` result; every new fixture writer must sit inside a try whose `finally` rmtrees the scratch.
3. network surface: `socket|urllib|requests|http` imports must stay 0.
4. host surface: `sysctl|pacman|systemctl|service|curl|wget` 0; no credential-looking strings (`password|token|secret|apikey`); os.environ reads limited to TMPDIR plus the pre-existing L67 passthrough.
5. injection: RC-8 is a pending OPERATOR decision — the value set reaching bash -c must remain EXACTLY `first_recheck()` output (first `recheck:` line, stripped). FAIL if the amendment ever executes a `restoration-recheck:` value, executes anything but the first recheck line, or interpolates file content into the command beyond that value. The both-headers fixture (check (iii) of C1) must classify as a normal entry with the restoration-recheck value never run — verify the amendment's classification branch reads `first_recheck(path) is None` before consulting `has_restoration_recheck`, i.e. restoration presence alone must not route any value to execution.
6. scratch: no `/tmp` literals beyond docstring prose; every `mkdtemp` call passes `dir=os.environ.get("TMPDIR") or None` (or the census's `env_tmp`).

Kill-rule relevance (reporting only, not judging): A5 (exec surface unchanged) is the
predicate this seat's re-run would evidence; an unfired SentinelC1 leaves A5 evidenced
only by the amendment author's own receipt.

## Bounds compliance

- Scratch root `/fast/scratch/hyaku/kasegi-r76/SentinelC1/` — used for the fetched base
  counter copy only; deleted before yield (rc reported at yield).
- Lane writes: this report file only (`Report:` trailer path honored, relative to the
  lane root). No lane edits, no git/jj mutations (only read-only `git show`), no network,
  no installs (none needed — nothing installed; PACMAN pause respected trivially).
- No evidence files beyond this report were needed; all numbers inline above.
