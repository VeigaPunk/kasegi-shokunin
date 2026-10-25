# CritNoHarm — round-26 wave-1 no-harm review (scoped findings)

Seat: CritNoHarm (read-only; no production edits). Lane: kasegi-shokunin.
Access date: 2026-10-25 (UTC). Base: `1b076fa7f2fb5e7dd9d87449514eba526043421b` (claims freeze).

Scope assigned: (1) recheck-audit.py `--expect` vs round-25 receipts (forward-only); (2) SOURCES.md S041 append + S040 recheck-cell update vs census invariant; (3) two knowledge entries + F11 row vs README invariants; (4) write-scope overlap via c4 ownership matrix. Verdict file: `wave1/k3-noharm.txt`.

---

## 1. recheck-audit.py `--expect` — round-25 receipts untouched (PASS)

Evidence:
- `git diff --name-only 41a77b8 HEAD -- .ufo/waves/round-25/` → **0 paths**; `git status --porcelain -- .ufo/waves/round-25/` → **0 lines**. The round-25 receipt subtree (3,773 tracked files) is byte-identical at freeze and now.
- Base instrument bytes (`git show 1b076fa:corpus/instruments/recheck-audit.py`, sha256 `c3c19adc…`) run against the round-25 frozen surface `.ufo/waves/round-25/c1-after-35` reproduce the round-25 receipt exactly: `lines=35 total=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`, `executes=12 gated=23 broken=0` — matches the round-25 lesson table.
- The planned change is additive: `--expect` defaults to `<root>/corpus/instruments/knowledge-expected.txt` (a path absent from every round-25 snapshot tree — verified its `/c1-after-35/corpus/instruments/knowledge-expected.txt` does not exist) and the instrument's own updated docstring states behavior is unchanged when `--expect` is absent or the file is missing. Round-25 receipt JSONs are never read, rewritten, or re-validated; the round-26 gate receipt is a separate file `.ufo/waves/round-26/c1-receipt-index.txt`.

Verdict: **no retroactive harm**. The change is forward-only, as required; it introduces a new pinned-expected-set gate for round 26 onward without altering what the round-25 receipts mean or any of their bytes.

## 2. Census invariant — BROKEN by the as-specified S041/S040 cells (FAIL)

Live (working tree already contains the ScribeSourcesAppend edit):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi  W04  S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi  W04  S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi  E09  S040 recheck=180d — final URL https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html (2 redirects); instrument UA required (browser UA 403s)
kasegi  E09  S041 recheck=180d — re-fetch with capture-source.py instrument UA (browser UA 403s); canonical anchor is the PDF
kasegi  E11  S041 missing used-by corpus/knowledge/iso-29147-and-30111-division-of-labour.md
kasegi  E11  S041 missing used-by corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md
$ echo $?
1
```

End-state scratch simulation (copy of `corpus/SOURCES.md` + real `corpus/knowledge/*.md` + stubs for the two planned entries, so the E11s clear): still **E09 S040 + E09 S041, exit 1**. The E09s are intrinsic to the cell text: contract E09 accepts only an ISO date, `NNd`, or a symbolic cadence (regex `^[0-9]+d$` / `^[A-Za-z][A-Za-z0-9 _-]*$`); prose after `180d` is invalid. So the census exits 1 even at round end — the C2 after-state `sources_census_exit=0` and the round-end census requirement would fail.

Smallest safe correction (simulated on the same scratch): keep the recheck cells cadence-only (`180d`) and move the R25-5 final-URL/UA prose into a `## Registry changes` note below the table → `validate` exit **0**, with only the pre-existing W04 S028/S029 warnings (same as round-25 close).

## 3. README invariants — broken by the F11 row's entry-cell names (FAIL)

- Frontier admitted count: the claims.json C2 awk now yields **11** (F11 row present) — that counter invariant holds.
- Entries-per-row: frontier table now lists 14 entry references (F01–F08: 8; F09: 2; F10: 2; F11: 2) — structurally consistent.
- Defect: the landed F11 row's entry cell cites the **staged package filenames** `knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md` and `knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md`, while the planned entries (w2/w3) are created as `iso-29147-and-30111-division-of-labour.md` and `iso-29147-divergence-and-clause-crosswalk.md` (no date suffix). `python3 corpus/instruments/frontier-recheck-count.py` therefore crashes:

```
FileNotFoundError: [Errno 2] No such file or directory: '.../corpus/knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md'
```

exit 1, immediately after the F11 row lands. The crash **persists** after w2/w3 create their files (different names) unless the F11 row is corrected to the actual filenames — or the entries adopt the staged names.
- Minor stale (doc, not machine-checked): README header correction line still records the round-25 count 37; after the two entries it should read 39.

## 4. Write-scope overlap — PASS (with two coordination hazards)

Consumed `.ufo/waves/round-26/wave1/c4-ownership.txt` and independently re-derived ownership from all 35 item prompts. No concrete path has two owners:
- `corpus/SOURCES.md` (w1); `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` (w2); `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` (w3); `corpus/README.md` (w4); `corpus/lessons/round-26.md` (w5); `SCORECARD.md` (w6); `LOG.md` + `PROVINCE.md` (w7).
- `corpus/instruments/recheck-audit.py` + `c1-controls/e1-selftest-live.txt` (e1); `corpus/instruments/knowledge-expected.txt` (e2); `c1-receipt-index.txt`/`c1-instrument-digest.txt`/`c1-live.json` (e3); `SKILL.md` (e4); `corpus/source-snapshots/round-26/S041.txt` (e5); `manifest.json` + `e6-recheck-results.txt` (e6); `c2-controls/do-nothing.json` (e7); `S040-live.txt` (s2 capture exception).
- `c1-controls/` partition: e1/m1 (`m1-*.txt`, `m1-summary.json`)/m2 (`m2-registry-mutants.txt`)/m3 (`m3-gameability.txt`) — distinct files; `c2-controls/m3-gameability.txt` (m3). MutRegistryRow is read-only on the real `SKILL.md`. Read-only seats write only their named wave1 report.

Observed coordination hazards (not overlaps):
1. **F11 name contract** (see §3): w4's README row and w2/w3's file creation disagree on filenames.
2. **Premature receipt index**: `.ufo/waves/round-26/c1-receipt-index.txt` and `c1-instrument-digest.txt` were written while the instrument was still at the round-25 digest (`instrument_sha256=c3c19adc…`, `selftest cases=14 failures=0 exit=0`). At review time the instrument bytes had since changed (observed digests: `503de028…` → `57efded2…` → `7f3f9671…`), so the committed index's digest line will not match the final instrument bytes unless re-written after e1 lands; the planned `selftest cases=15` (two new fixtures) has not landed yet — the current instrument still reports `cases=14`.
3. **Mid-edit broken states observed (snapshots, not final verdicts)**: at 09:35 the instrument did not parse (`IndentationError` line 173) and `--selftest` crashed (TypeError at line 245); at delivery it parses and `--selftest` runs 14 cases, `failures=0 exit=0`. ExecAuditFix is still writing; the receipt must be regenerated at the final digest.

## Smallest safe corrections (for the L1; not applied by this seat)

1. Census: S041/S040 recheck cells → `180d` only; R25-5 final-URL/UA prose → `## Registry changes` note (verified exit 0).
2. README F11 entry cell → the actual planned entry filenames (no date suffix), or align w2/w3 filenames with the row, so `frontier-recheck-count.py` can open them.
3. Re-write `c1-receipt-index.txt` after e1's change stabilizes, at the final instrument digest, with `selftest cases=15 failures=0` once the extended selftest passes (currently 14 cases; index digest is stale).

## Honesty note

All counts, exit codes, and quotes above were run/observed by this seat on 2026-10-25 UTC. The report records the wave's in-progress state at review time; peer seats may have changed the files since (executor edits observed mid-flight).
