# MutC2Counters — round-42 wave-1 receipt (C2 mutation probe)

Seat: MutC2Counters (mutation tester, leaf). Role spec: mutate each named C2
after-state on a scratch corpus copy; for each, name the frozen command that
must catch it and whether it does. Receipt-only; no lane deliverable file
(none was named — the report is this file). Claims frozen at
`.ufo/waves/round-42/claims.json` (read; untouched).

Scratch: `S=/fast/scratch/hyaku/kasegi-r42/MutC2Counters/` (created `mkdir -p`;
removed on exit after this receipt was written). Disk guard green at start:
`/fast/scratch/hyaku` 27% used, 590.8 G free.

## Fixture construction (the "C2 after-state" I mutated)

The live lane at `kasegi-shokunin` is still at the C2 BEFORE state (verified
2026-10-28 ~08:1x UTC): frontier 24, F25 rows 0, registry 63, S064 rows 0,
entries citing S064 0, knowledge 60 — matching `c2-controls/before.txt`
exactly. So the "each C2 after-state" target did not exist in the lane to
copy; I built it on a scratch copy instead:

```
S=/fast/scratch/hyaku/kasegi-r42/MutC2Counters
cp -a $LANE/corpus $S/lane/corpus ; cp -a $LANE/PROVINCE.md $S/lane/
+ corpus/source-snapshots/round-42/S064.txt   (5 lines, SYNTHETIC fixture
  bytes — NOT a network fetch; declared so because source-recheck needs a
  byte-pinned file and no real OSV capture exists yet)
+ corpus/source-snapshots/round-42/manifest.json  (schema_version 1, one
  record: id=S064 path=S064.txt url=https://ossf.github.io/osv-schema/
  fetched_utc=2026-10-28T13:00:00Z sha256=<file>, quotes Q1/Q2 pinned to
  verbatim lines with anchors 3/4 — mirrors round-41/manifest.json shape)
+ corpus/knowledge/osv-schema-vulnerability-record-format.md
  (source: S064 / verified-at: 2026-10-28 / recheck: cd $S/lane &&
  python3 corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-42/manifest.json --source S064;
  prose cites S064.txt:3,:4,:5; evidence bullet `- S064 —`)
+ corpus/SOURCES.md: `| S064 | … | spec | A | … | mined | 2026-10-28 |
  on-release | corpus/knowledge/osv-schema-vulnerability-record-format.md |`
  inserted directly after the S063 row
+ corpus/README.md: `## Round-42 admission …` section appended at EOF
  (r41-style: id/topic/status/entry/sources/next table + `| F25 | … |
  admitted | knowledge/osv-schema-vulnerability-record-format.md | S064 |`
  row + `frontier stands at **25/25 admitted**` amendment paragraph)
+ PROVINCE.md: `[r42 Frontier amendment, appended 2026-10-28, …] F25 — …`
+ corpus/instruments/knowledge-expected.txt: new entry path added
  (sorted order preserved)
```

Entry `recheck:` uses `cd $S/lane` (absolute) because the audit's `cwd` limb
runs the line at root AND at `/` — a relative-path recheck diverges there;
real entries cd to the lane absolute path for the same reason. This makes the
fixture's audit require `--cdroot` care (noted per command below).

## Baseline: frozen commands on the pristine after-state (before mutations)

All nine frozen counting commands were run against `$S/lane`:

| # | frozen command (spec) | pristine output | matches after-value? |
|---|---|---|---|
| C1 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `25` | yes (24→25) |
| C2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `64` | yes (63→64) |
| C3 | `awk -F'|' '/^\|[[:space:]]*S064…/ {s=$9; gsub(//,""); if(s=="mined") n++} END{print n+0}'` | `1` | yes (0→1) |
| C4 | `grep -rlE '^source: S064' corpus/knowledge | wc -l` | `1` | yes (0→1) |
| C5 | `ls corpus/knowledge/*.md | wc -l` | `61` | yes (60→61) |
| C6 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=28 pass=28 exit=0`, `PASS F25 … ids=S064 exit=0` | yes |
| C7 | `python3 corpus/instruments/capture-binding-check.py` | `records=56 bound=56 unbound=0` exit 0 | yes (55→56) |
| C8 | `python3 corpus/instruments/recheck-audit.py --quiet` | `lines=61 total=61 pass=61 expected=61 missing=0 unexpected=0` | yes — see note |
| C9 | `bash scripts/sources-census.sh validate --root <fleet> kasegi` | replayed faithfully as `validate --file $S/lane/corpus/SOURCES.md` → `file ok`, only standing `W04 S028/S029`, exit 0 | yes |

Notes on C8/C9 replayability:
- C8's output header on the scratch copy is `strict pass=60/61
  cdroot_fail=1 … exit=1`: the audit's `cdroot` strict limb demands recheck
  lines cd into `--cdroot` (default = `--root` = scratch); my fixture entry
  cds to `$S/lane` so the limb is green under `--cdroot $S/lane` and the 60
  inherited entries (which cd to the real lane) go red, or vice-versa. All
  printed numbers and `expected=61 missing=0 unexpected=0` are identical in
  both modes; on the real lane at Y the frozen form prints exit 0. For
  mutation deltas I ran `--root . --cdroot <real-lane>` (60/61 baseline,
  single known cdroot artifact = my fixture entry) — deltas below are real.
- C9's frozen form is pinned to `--root <fleet-root>` lane `kasegi`; a
  faithful scratch replay is `validate --file <registry>` (script derives
  the lane dir from the file's parent corpus dir). The lane-level command
  was not run against the real lane (would test the unmutated real registry).

`python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-42/manifest.json --source S064` on pristine:
`S064:sha256 OK`, `S064:Q1 OK occurrences=1 anchor=3-ok`, `S064:Q2 OK
occurrences=1 anchor=4-ok`, exit 0 — the manifest record passes its recheck.

Pristine hashes (the files mutations touched):
`README.md` bcdeb1ebe95205e5077d594e2952674315854ff713f2e140a931d06d05593e43
`SOURCES.md` 401aadf51d56cc6f9061704c4adbc20f5da6bdcc7c51de1c96e04a98c258aed5
`osv-schema-…-format.md` a9127aa661ac81e84621e8162b1623278fd4d1e731676c39ecf66576e59a5cb2
`knowledge-expected.txt` 7da7f7e37667c58c7b8352de2bf724be10d483bd5a886bb84e2f2c9fc4610400
`round-42/S064.txt` c0fc4e9ae3cd328946cdef30fd0e9ab8292969f663c69124b8d48be28f3bb06c
`round-42/manifest.json` e4534e23f5710216957c4d2378ce899fa88701b4607d90b851b714d2370853be

## Mutations — mutant, expected detector, actual output, verdict

### M1 — "frontier row 24->25 without PASS"
Mutant: README F25 row's status cell `admitted` → `queued` (row still present,
still greppable). Mutated sha `94d7fd1e…aba52c` (pristine `bcdeb1eb…`).

| frozen command | expected to catch? | actual output | verdict |
|---|---|---|---|
| C1 grep rows | NO — row shape intact | `25` | survived (prints after-value while defect is live) |
| C6 harness | YES — `entries=28 pass=28` + `PASS F25` required | `entries=27 pass=27 exit=0`; no F25 line at all (status filter skips non-`admitted`) | **KILLED** (entries 27≠28; exit=0 without PASS F25, caught also by kill_rule "status cell not admitted" / "no PASS F25 line") |
| C7 binding | no | `records=56 bound=56 unbound=0` | survived |
| C8 audit | no | `lines=61 total=61 pass=61 expected=61 …` unchanged | survived |
| C9 census | no | `file ok`, exit 0 | survived |

Verdict: KILLED by C6. C1 alone cannot see this defect — the harness's
`admitted`-filter is the only frozen limb that reads the status cell.
Restored: `cp -a $S/pristine/lane/corpus/README.md` → sha `bcdeb1eb…` ==
pristine (verified).

### M2 — "registry 63->65 with a queued S064"
Mutant: S064 status cell `mined`→`queued`; appended rejected row `| S065 |
CVE Record Format 5.x … | rejected | 2026-10-28 | on-release | — |` after it
(registry → 65 rows). Mutated sha `ee277152…` (pristine `401aadf5…`).

| frozen command | expected to catch? | actual output | verdict |
|---|---|---|---|
| C2 grep rows | YES (65≠64) | `65` | **KILLED** |
| C3 awk mined | YES (0≠1) | `0` | **KILLED** |
| C6 harness | no | `entries=28 pass=28 exit=0` incl `PASS F25` | survived — harness reads entry+manifest, never the registry status |
| C7 binding | weak | `records=56 bound=56 unbound=0`; `MANIFEST round-42 records=1 url_bound=1` | **survived — blind spot**: rule B3 only refuses `rejected` anchors; a `queued` row still anchors a bound capture record (queued+mined are treated identically) |
| C8 audit | no | `lines=61 … expected=61` | survived |
| C9 census | partial | `file ok` exit 0 — `queued`/`rejected` are both valid statuses; census reports no E-code for a queued row holding a capture+entry | survived |

Verdict: KILLED by C2 and C3. Coverage note: nothing among the commands
checks that a `queued` (or `rejected`) registry row cannot anchor a live
capture manifest — the mined-status predicate is enforced only by the C3
awk cell-grep, and the "S065 rejected screen row" half is invisible to every
instrument (row-count parity is the only guard). Restored: `cp -a` →
`401aadf5…` == pristine, `grep -cE 'S065'` = 0 (verified).

### M3 — "entry citing S064 without recheck line"
Mutant: removed ONLY the `recheck: cd $S/lane && python3
corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/
round-42/manifest.json --source S064` line; `source: S064` and prose intact.
Mutated sha `3776433a…` (pristine `a9127aa6…`).

| frozen command | expected? | actual | verdict |
|---|---|---|---|
| C4 grep source | NO | `1` | survived (after-value printed with defect live) |
| C5 ls | NO | `61` | survived |
| C6 harness | YES | `FAIL F25 … ids=S064 exit=- problems=no-recheck-line,no-source-selection,no-manifest` → `entries=28 pass=27 exit=1` | **KILLED** |
| C8 audit | YES | `lines=60 total=61` (completeness gap), `expected=61 unexpected=0`, exit 1 | **KILLED** (60≠61) |
| C7 binding | no | `56 bound=56` | survived |
| C9 census | no | exit 0 | survived |

Verdict: KILLED by C6 and C8. Restored → `a9127aa6…` == pristine.

### M4 — "knowledge 61 without source: trio"
Mutant: removed all three trio legs (`source: S064`, `verified-at:
2026-10-28`, `recheck:`) from the new entry; the file remains (61 files).
Mutated sha `d565511d…`.

| frozen command | expected? | actual | verdict |
|---|---|---|---|
| C4 grep source | YES (0≠1) | `0` | **KILLED** |
| C5 ls | NO — file exists | `61` | survived (after-value printed with defect live) |
| C6 harness | YES | `FAIL F25 ids=- exit=- problems=no-source-line,no-recheck-line,no-source-selection,no-manifest` → `entries=28 pass=27 exit=1` | **KILLED** |
| C8 audit | YES | `lines=60 total=61`, exit 1 | **KILLED** |
| C7 binding | no | `56/56` | survived |
| C9 census | no | exit 0 | survived |

Verdict: KILLED by C4, C6, C8. Restored → `a9127aa6…` == pristine.

### M4b (bonus, minimal trio variant) — drop ONLY `verified-at:`
Mutant: removed just `verified-at: 2026-10-28`; `source:` + `recheck:` intact.
Mutated sha `b9b0f287…`.

| frozen command | actual | verdict |
|---|---|---|
| C4 | `1` | survived |
| C5 | `61` | survived |
| C6 | `PASS F25 … entries=28 pass=28 exit=0` | survived |
| C7 | `56 bound=56` | survived |
| C8 | `lines=61 total=61 pass=61 expected=61 …` | survived |
| C9 | exit 0 | survived |

Verdict: **SURVIVED all nine frozen commands** — a coverage finding, not a
contract change: the provenance trio's `verified-at` leg has no counting
command behind it; enforcement exists only as kill_rule text ("lacking the
provenance trio"). A wave-2 attack receipt could exploit this only by
claiming C2 while dropping `verified-at` — caught by the kill clause alone.
Restored → `a9127aa6…` == pristine.

### M5 — "binding 56/56 with one unbound"
Mutant: `corpus/source-snapshots/round-42/S064.txt` moved out of the dir
(manifest record intact: id/path/url/fetched_utc/sha256/quotes all valid).
This is the documented blind spot: binding binds record→row (B) and
provenance (C); nothing checks record→capture-file existence.

| frozen command | expected? | actual | verdict |
|---|---|---|---|
| C7 binding | under test | `MANIFEST round-42 records=1 url_bound=1 fetched=1`; `records=56 bound=56 unbound=0` exit 0 | **SURVIVED — confirmed blind spot** (manifest's `files:["S064.txt"]` and `path:"S064.txt"` unchecked against the directory; capture absence not a rule) |
| `source-recheck.py --manifest …/round-42/manifest.json --source S064` (the predicate's own recheck gate) | YES | `S064:source UNAVAILABLE reason=missing` exit 2 | **KILLED** |
| C6 harness | YES — it *executes* each entry's recheck | `FAIL F25 ids=S064 exit=2 problems=recheck-exit-2` → `entries=28 pass=27 exit=1` | **KILLED** |
| C8 audit | weak | `lines=61 total=61 pass=61`; entry class flips `executes`→`gated` (`fail-closed 24→25`); `gated` is not a verdict | survived as verdict, listed as fact |
| C9 census | no | exit 0 | survived |

Verdict: **SURVIVED the named frozen binding command; KILLED by the harness
(and by any execution of the entry's own recheck)**. Net kill-rule outcome:
caught — `capture failing source-recheck` and `harness not pass=28` both
fire. But the specific claim text "`binding 56/56`" cannot distinguish
bound-record from present-capture; the `records=`/`bound=` invariant is a
record-to-registry binding, not a record-to-file one. A lane landing a
manifest without the capture would pass C7 green and die only at C6.
Restored: `mv` back → `c0fc4e9a…` == pristine.

## Summary table

| mutant | C1 | C2 | C3 | C4 | C5 | C6 harness | C7 binding | C8 audit | C9 census | net |
|---|---|---|---|---|---|---|---|---|---|---|
| M1 F25 no-PASS (status queued) | SURV | – | – | – | – | KILL | SURV | SURV | SURV | KILLED |
| M2 registry 65, S064 queued | – | KILL | KILL | – | – | SURV | SURV | SURV | SURV | KILLED |
| M3 entry no recheck line | – | – | – | SURV | SURV | KILL | SURV | KILL | SURV | KILLED |
| M4 entry no trio | – | – | – | KILL | SURV | KILL | SURV | KILL | SURV | KILLED |
| M4b drop only verified-at | – | – | – | SURV | SURV | SURV | SURV | SURV | SURV | **SURVIVED ALL** |
| M5 bound record, capture absent | – | – | – | – | – | KILL | SURV | SURV | SURV | KILLED (via C6+recheck, not C7) |

(SURV = mutant survives that command; KILL = command's required output/exit
falsified; "–" = command doesn't read that surface.)

## Findings for the ledger

1. All five spec'd mutations are killed by at least one frozen command. The
   claim's counting-command battery is adequate to its kill clauses for the
   mutated defects.
2. Two genuine coverage gaps observed, both already consistent with the
   kill_rule text but with no instrument backing:
   a. `verified-at:` (and the "opened this round" recency cell of a mined
      row) — no frozen command reads either field.
   b. capture-binding `unbound=0` does not bind a record to the *existence*
      of its capture file (documented limitation, confirmed live: exit 0 on
      a manifest whose `path` names a missing file). The net catch depends
      on C6 executing each entry's recheck — a lane where the F25 entry's
      recheck line were missing AND the capture absent would need the M3
      path (no-recheck-line) to fire; both limbs were separately verified.
3. Cross-check value confirmed: C1's grep prints the after-value 25 while
   M1's defect is live — only the harness's admitted-status filter catches
   it; C4's grep prints 1 while M3's defect is live — only the harness +
   audit completeness catch it. The counters alone are not the detector;
   the executable gates are.

## Restoration evidence

- After every mutation the mutated file(s) were `cp -a`-restored from
  `$S/pristine/lane/`; sha256 of each restored file equals the pristine hash
  listed above (recorded inline per mutation).
- Final whole-tree check: `diff -r $S/lane $S/pristine/lane -q` →
  `IDENTICAL` (no output but the marker). Every mutated file byte-identical.
- Nothing written outside `$S` except this receipt. No git/jj command run
  anywhere; no lane file touched. Lane repo read-only throughout.

## Tools installed

None. Used only: bash, cp/mv/sha256sum/diff/grep/awk/ls, python3 (fixture
writes + instrument invocations), `sources-census.sh` in `--file` mode.
No network fetches (S064 capture bytes are synthetic fixture content,
declared above; no URL was fetched).

## Limits of this probe

- The fixture's S064 capture is synthetic; a real OSV fetch would change the
  sha256 pins, not the detector relationships measured here.
- C9's frozen `--root <fleet>` form was not rerun against the live lane
  registry (it's read-only against real lane; `--file` is the faithful
  scratch replay and exited 0 on the valid statuses).
- M2's `queued`/`rejected` statuses are contract-valid; the mutation's
  defect is the *claims-level* requirement (S064 must be `mined`, registry
  must be 64+R where R counts by the mined-awk) — caught by C2/C3 as shown.
