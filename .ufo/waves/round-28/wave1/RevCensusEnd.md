# RevCensusEnd — round-28 wave-1 round-end census verification (C2 registry gate)

Role: reviewer (coverage). Scope: `corpus/SOURCES.md` census conformance at round end —
maintained `sources-census.sh validate` plus the seven frozen manual commands from
`CORPUS.md` §Census (fleet root `/home/vgpnk/Projects/shokunin/CORPUS.md:131-148`).
Read-only seat: zero production edits; this file is the only write.
Tools: stock GNU bash 5.3.20, gawk 5.4.1 — nothing installed or upgraded.
All commands run from lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, 2026-10-25 UTC.
State at run time: uncommitted working tree (L1 has not committed wave-1 yet);
`corpus/SOURCES.md` modified vs HEAD `94f387cbee71a532a51ce075f01701a557231e85`.

## Rows before vs after (counting command)

Command: `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
(live bytes: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`)

- before = **41** at claims-freeze commit `c9f8b115…` (lane base; measured) — also 41 at
  `claims.json.base` `261a6651…` (measured); both equal the frozen `before.sources_rows=41`.
- after = **42** in the working copy (measured post-landing); expected 42 — **match**.
- S042 row counter `grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md` → **1**
  (matches the C2 counter's `after` expectation).

## Canonical validate — full output + exit code

`$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`

```text
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Verdict: **exit 0** — the C2 predicate "census exit 0" holds on the landed working copy.
The two `W04` lines are pre-existing (same pair recorded in
`.ufo/waves/round-27/census-before.txt` per `corpus/lessons/round-27.md`), are warnings
not E-codes, and never move the exit code.

## Seven frozen manual census commands — verbatim outputs

`$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`  (rows)
```text
42
```

`$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md`  (malformed; must print 0)
```text
0
```

`$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md`  (tier histogram)
```text
A=39 B=1 C=2 
```

`$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md`  (status histogram)
```text
mined=30 queued=9 rejected=3 
```

`$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d`  (duplicate ids; must print nothing)
```text
(empty)
```

`$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md`  (enum/tier inflation; must print nothing)
```text
(empty)
```

`$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done`  (mined used-by paths exist; must print nothing)
```text
(empty)
```

Supplemental E12 sanity (not in the frozen seven; matches maintained-parser scope):
all `S###` table rows occur under `## Registry`; no row-shaped lines in other sections.

## Findings by severity

- **Resolved transient (Low; no residual defect):** E11. I began before ScribeEntryC2
  landed; with `SOURCES.md` already carrying S042 and S041's extended `used-by` but
  `corpus/knowledge/japanese-domestic-disclosure-workflow.md` still absent,
  `validate` printed `E11 S041 missing used-by …` + `E11 S042 missing used-by …`,
  exit **1**; CMD7 printed `missing: …` twice. After the entry landed (~17:2xZ),
  re-runs give exit 0 and empty CMD7. Transient intra-wave ordering artifact, not a
  landed defect — but it proves E11 is load-bearing against exactly the C2 race, and
  the L1 commit must include the entry bytes or the committed tree fails the gate.
- **Pre-existing (Informational):** W04 S028 + W04 S029 (same URL across scopes).
  Unchanged since round 27; warnings only.
- **Documentation nit (Informational, not a census defect):** `claims.json` field
  `base` = `261a6651…` (r27 spot-check), while the lane base/claims-freeze commit is
  `c9f8b115…` (HEAD~1 at run time). Both trees yield rows=41, so the frozen
  `before` value is unaffected; noted so a later reader does not take `base` for the
  freeze commit.

## Cell-level spot-checks on the new/changed rows (census-adjacent)

- S042 row: `id S042`, `kind docs`, `tier A`, `status mined`, `opened 2026-10-25`
  (not future → E08 clean), `recheck 180d` (E09 clean), `used-by` =
  `corpus/knowledge/japanese-domestic-disclosure-workflow.md` exactly — matches the
  frozen C2 shape (tier A, mined, opened 2026-10-25, used-by exactly the entry).
- S041 `used-by` old→new logged in `## Paths`: `…iso-29147-divergence-and-clause-crosswalk.md`
  → same `, corpus/knowledge/japanese-domestic-disclosure-workflow.md` appended (R8-conformant
  log line present in the diff); every other S041 cell byte-identical.
- S042 row was rewritten into lane cell shape (scribe log discloses the staged row's
  `ウェブアプリケーション … steps 1 to 6` anchor claim was not carried — the round-28
  capture shows 7 steps). Census verifies shape only; content grounding is other seats'.
- Cross-references (judged-on coverage, adjacent evidence): F12 README row
  `| admitted |` naming `knowledge/japanese-domestic-disclosure-workflow.md`, sources
  `S041, S042`; frontier admitted count counter = **12**; `grep -lE '^source: S042 '`
  → exactly the entry (1 file). Entry `source:` headers carry S041 + S042; recheck
  line is a single `cd <lane-root> && …` command citing `--source S041` and
  `--source S042` against `corpus/source-snapshots/round-28/manifest.json`.

## Residual risk / verification gaps

- Measured on **uncommitted** bytes: `SOURCES.md` is ` M` vs HEAD `94f387c`. The L1
  commit will land this file plus the entry and the manifest/captures in one commit;
  if the commit splits them, the intermediate tree fails E11. Re-run command after
  the L1 commit, from the lane root:
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?`
  (expected: W04×2 + `ok`, exit 0) and the CMD7 mined-used-by awk above (expected: empty).
- Census conformance ≠ content truth: tier/anchor/step-count accuracy of the S042 row
  text is not exercised by any of the eight checks; relied on ScribeRegistryC2's
  disclosed rewrite. A fabricated-but-well-formed row passes this gate — known,
  contract-scoped gap, not new.
- `uniq -d`/`empty` outputs were captured verbatim; `cmd*_exit=0` (no signal).
- E04 duplicate-URL: none new (S042's IPA URL is unique; S043 staged = lane S041 was
  cited not re-registered, so no second JPCERT row exists to trip E04).

**Verdict (recommendation, not admission):** census gate satisfied post-landing —
rows 41→42, malformed=0, no duplicate ids, enums clean, no tier inflation, all mined
used-by paths resolve, maintained validate exit 0 with only pre-existing W04s.
No conformance defect stands at end-state. The E11 transient names the one landing
order that would fail: registry-before-entry must not be the committed shape.
