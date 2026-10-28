CritSync — round 42 wave 1 — receipt-only C2 integration-edge attack.
Lane HEAD at review time: 0566bd6 (C2 deliverables not yet landed; wave1 holds RevLessonShape.md + ScribeScorecard.round42.txt only). The attack therefore targets the verification architecture that will judge the C2 build: the frozen claims' counting commands/kill clauses plus the committed instruments of record. claims.json read first (frozen_by KasegiR42, base 5053a7f, errata list empty). Baseline parity with c2-controls/before.txt confirmed live: F rows 24, S rows 63, mined-S064 0, entries citing S064 0, knowledge files 60, harness `entries=27 pass=27 exit=0`, binding `records=55 bound=55 unbound=0`, audit `expected=60 missing=0 unexpected=0`, census `exit=0` with exactly the two standing W04s (S028/S029).

## Edge 1 — entry lands before its S064 row: what the harness sees

`PASS F25` and `entries=28 pass=28 exit=0` — even with no S064 row anywhere.

Evidence: `frontier-recheck-count.py` `evaluate()` (lines 179-240) and `entry_contract()` (lines 106-160) read only the entry file, the manifest named by its `recheck:` line, and the subprocess result. `SOURCES.md` is never opened; no limb checks that a declared/cited S-id exists as a registry row. Proof by construction: the instrument's own selftest fixtures (`build_fixture`, lines 280-307) write a README row, an entry, a manifest and a stub `source-recheck.py` — and never write `corpus/SOURCES.md`; `python3 corpus/instruments/frontier-recheck-count.py --selftest` prints `selftest cases=6 failures=0` on my run. So `PASS F25` is not evidence the S064 row exists; the harness only proves entry↔manifest↔recheck coherence.

Composed claim still rejects the attack — contained:

- `bind_record` (capture-binding-check.py:283-305) returns `rule=no-row` when `rows_by_id` lacks the record id → output `records=56 bound=55 unbound=1` → kill clause "capture-binding unbound!=0". The `case_no_row` selftest fixture (lines 575-577) is committed for exactly this shape.
- Independent kill clause "no S064 row opened this round" + counting command `awk ... status=="mined"` on S064 → 0.
- If the row is skipped AND the manifest record is skipped too: binding stays 55/55 (no record to bind), but the same S064 clause and `grep -> 63` counting command still fire.

Residual defect (minor, duplicate authority): the README row's `sources` cell is unverified — `FRONTIER_ROW` (line 86) captures only id/title/status/entry; the 5th cell naming `S064` is never parsed by any instrument. An F25 row could carry `—` or a wrong S-id there and pass everything; only the entry's `source:` lines bind the id.

## Edge 2 — manifest record bound but capture unreadable

Demonstrated instrument blind spot, backstopped claim-side.

Fixture (`/fast/scratch/.../fix-lane`, removed after copy): one mined S001 registry row, one schema-1 round-99 manifest with one record (url matching the row, fetched_utc valid), and **no S001.txt on disk**. Live run:

```
MANIFEST round-99 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=1 ... orphans=0
records=1 bound=1 unbound=0
exit=0
```

`bind_record` verifies id-exists-in-registry, status!=rejected, url-match — and nothing else; `check()` (lines 434-444) only iterates capture files that exist (orphan detection) and `declared - captures` for manifest-listed orphans. A record's own `path` is never opened. Consequence: the frozen counter `records=56 bound=56 unbound=0` can be printed with the S064 capture absent or unreadable — `bound` does not imply a readable capture exists. Latent false-provenance in the instrument's printed headline.

Backstop confirmed live: `python3 corpus/instruments/source-recheck.py --manifest <fixture> --source S001` → `S001:source UNAVAILABLE reason=missing`, exit 2 (lines 156-169: FileNotFoundError→missing, OSError→unreadable). Kill clauses "its capture failing source-recheck" and "junk twin accepted (a mined-marked row without capture+entry+harness pass)" fire; the harness entry recheck also fails with `recheck-exit-2` → FAIL. Composed verdict: red — but through source-recheck, not through binding.

Smallest safe correction (instrument, not claim): add `rule=path-missing`/`rule=path-unreadable` limbs — for each record, require `<snapdir>/<record.path>` to be a readable regular file before the record can count as bound; emit it as FAIL rather than relying on the orphan machinery. Closes the only gap where binding is the sole capture-presence limb.

## Edge 3 — rejected S065 counted as registry growth?

Yes — and that creates a frozen-counter defect. Any `| S### | … |` table row matches the counting grep `^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|` regardless of status; the lane carries 10 rejected rows today (S022, S024, S026, S027, S028, S056, S058, S059, S061, S062 — awk `$9` status `rejected`, verified live) inside the 63. Precedent is explicit (SOURCES.md:134-137): the r38 append took the registry 55→59 counting "the mined S057 row plus the rejected S056, S058 and S059 rows". The claims summary likewise states `registry 63 -> 64+R (R>=1)`.

So with the required rejected screened row committed as a table row, the actual value is 65, but the frozen counting command (claims.json C2) reads:

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 63 -> 64
```

`64` is unreachable under the claim's own build (R>=1 → ≥65). No kill clause checks the registry count, so a literal reading either wrongly fails a compliant J or silently expects the rejected row to live somewhere else (contradicting convention and the claim's own `64+R`). This is the strongest counterexample found this pass: the frozen counter and the frozen claim text disagree.

Smallest safe correction: use the existing `errata` channel (claims.json carries `"errata": []`) to amend the expected string to `63 -> 64+R` (or `>=65`), and add the companion status probe `awk -F'|' '/^\|[[:space:]]*S065[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); if(s=="rejected") n++} END{print n+0}' -> 1` so the reject row is counted AND status-verified, not just present.

Sub-checks that hold: (a) mis-numbering — if the rejected row takes S064 and the mined row S065, `awk S064 mined`→0 and kill "no S064 row" fire; red, correctly. (b) A rejected S065 whose URL duplicates an existing row **across scopes** prints a NEW W04 → kill "census … or a new W/E code" fires even though census exits 0 — builders must screen the reject URL against url_scopes. (c) E11's used-by existence check runs only for `status==mined` (sources-census.sh `usedby_findings`, `[ "$status" = mined ] || continue`) — a rejected row's dangling used-by is never checked; harmless today (`—`) but asymmetric with E11's intent.

## Edge 4 — PROVINCE amendment without the README row

The assigned direction is contained: `grep F rows` → 24≠25, harness `admitted`-filter (main, line 393: `r[2] == "admitted"`) → `entries=27`, kill clause "no F25 frontier row or its status cell not `admitted`" fires.

The real defect is the mirror image: **README row landed, PROVINCE amendment missing** —

- Predicate requires BOTH ("with a coverage-map row in corpus/README.md and an appended F25 amendment in PROVINCE.md").
- The kill rule names only the README side. Nothing in the kill rule, counting commands, or instruments mentions PROVINCE: `grep -rn PROVINCE corpus/instruments/*.py scripts/sources-census.sh` → no consumers of the amendment (only r38/r39 suite fence-shape scans, not presence). The amendment line `[rNN Frontier amendment, appended …] FNN — …` (PROVINCE.md:74-80,156-163 convention) is greppable one-line text — cheap to count, currently uncounted.
- A J with `| F25 | … | admitted | …` and no r42 amendment line yields every counter green — 25 rows, `PASS F25`, 28/28, census 0 — while the predicate is false. Predicate limb unobservable → wrong-admit risk; the r39-r41 rejected closures failed on exactly this class of thin verification surface.

Smallest safe correction: one counting command `grep -c '^\[r42 Frontier amendment.*F25' PROVINCE.md -> 1` (or the matching kill clause "no appended F25 amendment line in PROVINCE.md"). Deterministic, single line, matches five rounds of precedent shape.

## Verdicts

| Edge | Counterexample outcome | Claim-safe? |
|---|---|---|
| 1 entry-before-row | harness prints PASS F25 + 28/28 (registry-blind by construction); binding `rule=no-row` + S064 clause kill it | Yes — contained; note PASS F25 ≠ row existence |
| 2 bound-but-unreadable | `bound=1 unbound=0` on absent capture (fixture-verified); source-recheck UNAVAILABLE kills | Claim red; instrument overstates `bound` — add path-existence limb |
| 3 rejected S065 | grep counts it (65 actual) but frozen counter expects 64 | **Defect**: unreachable expected value; fix via errata `63 -> 64+R` + status probe |
| 4 PROVINCE-only | grep/harness/kill all red — contained | Yes; but inverse (README-only, no amendment) is an unkillable predicate limb — add counted grep |

Impacted axes: depth:verifiability (frozen-counter truthfulness, kill-clause completeness — both defects are fixable pre-J via the errata channel or verifier-side counted commands), coverage (C2 admission wiring is otherwise sound: all four assigned attacks land red or stay consistent with convention). No attack on the F25 topic choice itself — scout screen not yet landed; wave-2 falsifiers should re-check "chosen topic's document already covered" against the actual OSV/CVE-Record pick once committed.

No tools installed (all checks ran with repo/python3/bash/gawk already present). Scratch `/fast/scratch/hyaku/kasegi-r42/CritSync` removed at yield; fixture root `fix-lane` + selftest dirs `hs*` lived only there.
