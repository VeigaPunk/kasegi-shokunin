# R44Critic11 — C2 frontier novelty, attacked against the 25 admissions and the lane's own standards

Seat item: *Challenge C2 frontier novelty against existing 25 admissions and every nearby standard in
lane corpus.* Read-only. No production edit, no commit, no git/jj/index mutation, no pacman, no tool
install. Measured 2026-10-28T19:05–19:14Z over the working tree of
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` at `HEAD=66314015122b9aa32dc40f2f1815df56624c26d1`
(frozen base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`, control `controls/do-nothing.txt:2`).

**Verdict in one line:** F26 is *absent at base and reachable*, so C2's "absent" premise holds; but the
landed F26 is **not a new practice** — 3 of its 4 load-bearing rows restate rules already admitted
under F01/F03/F09/F13, the one genuinely absent rule is a minor sub-clause, and the capture's strongest
novel rule (customer IP-range ownership) was left out. C2's after-state is therefore a *vendor-instance*
credit, not the "source-grounded frontier move" its `after` cell implies, and the frozen counter that is
supposed to prove it cannot print 25 or 26 at all.

## 1. Counterexample — the overlap is 3 of 4, with exact bytes

The F26 entry's substance is a four-row claim table,
`corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md:13-18`. Each row against the nearest
admitted rule:

| F26 row (file:line) | Rule it states | Already admitted at |
|---|---|---|
| `:15` scope statement ≠ permission ("not permission to test an arbitrary Google-branded or customer-owned service", `:9`) | a program's scope indicator does not add assets or grant permission | `knowledge/authorization-safe-harbor-and-scope.md:8` — "A safe-harbor badge or statement alone does not add assets to scope or establish permission for an action that the program's policy excludes." (F03) |
| `:16` customer-owned resources prohibited | a program can only place assets it controls in scope; third-party/customer assets are not authorized | `knowledge/program-severity-ladders-and-reward-scales.md:16` — "Third-party assets outside HackerOne's control are not authorized for testing because HackerOne cannot grant permission to test infrastructure it does not host or operate." (S043.txt:40, F13); and `knowledge/statutory-authorization-and-unauthorized-access.md:46` — "Where the asset is operated by a third party (a customer, a supplier, a hosting tenant), the platform's text cannot supply that third party's consent" (F09); and `knowledge/doj-vdp-framework-scope-and-authorization.md:40-48` — "Absent an agreement with the cloud service provider, the organization implementing the vulnerability disclosure program may lack the authority to authorize others" (S020, tier A) |
| `:17` reward ineligibility separate from technical validity | technical score vs the program's eligibility/reward criteria | `knowledge/cvss-v4-severity-and-vector.md:34` — "Keep the report's technical score and vector distinct from the program's own severity, eligibility, and reward criteria." (F01) |
| `:18` multi-tenant escapes: test in isolated/local environments, do not test the live multi-tenant environment | **no prior occurrence in the corpus** | none — see §2 |

So three of the four rows are re-statements of admitted rules, and the F26 row's own `next` cell
(`corpus/README.md:628`) names as its distinguishing instruction exactly those three rules:
"Keep the Cloud VRP boundary distinct from general authorization, other Google reward programs, and
customer permission". It distinguishes F26 from F03/F09/F10 by *restating* them; it names no new
practice. The S069 registry row's `teaches` cell (`corpus/SOURCES.md:75`, column 7) does the same —
"limited to Google-owned infrastructure, prohibits customer-resource testing, and makes reports
ineligible" — the three duplicated rules, no novelty claim.

Command (single-line, reproducible):

```
sed -n '8p' corpus/knowledge/authorization-safe-harbor-and-scope.md
sed -n '16p' corpus/knowledge/program-severity-ladders-and-reward-scales.md
sed -n '46p' corpus/knowledge/statutory-authorization-and-unauthorized-access.md
sed -n '34p' corpus/knowledge/cvss-v4-severity-and-vector.md
```

## 2. Counterexample — the one absent rule is not the one the row claims, and the capture's best new rule is omitted

Absence of the tenant/reproduction rule, over the whole lane prose corpus (excluding captures):

```
$ grep -rniE 'multi-tenant|shared tenant|live tenant|local reproduction|reproduce (locally|it locally)' \
    corpus/knowledge corpus/README.md corpus/PROVINCE.md corpus/QUALITY.md SKILL.md
corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md:18: ...   # the new entry itself
corpus/knowledge/ufo-archive-2026.md:153: ... "documented multi-tenant   # unrelated historical quote
```

That rule is real in the capture: `corpus/source-snapshots/round-44/S069.txt:78-87` — "do **not** test
it against the live multi-tenant environment. Instead, submit a report with your technical analysis and
local reproduction" (the entry cites the same span as `:78-86`). It is the only row of the entry that
is corpus-new, and it is one table cell.

Meanwhile the capture's **strongest genuinely new rule is not in the entry at all** —
`S069.txt:73-77`: "*Customer IP Ranges*: Scanning CIDR blocks or IP ranges allocated to Google Cloud
customers … is prohibited. Finding a Google-owned asset inside a customer IP block during a broad scan
is still considered unauthorized testing within customer space." Zero occurrences anywhere in the lane
prose:

```
$ grep -rniE 'cidr|customer ip|ip ranges|allocated to (google )?cloud customers' \
    corpus/knowledge corpus/README.md SKILL.md corpus/PROVINCE.md
(no output, rc=1)
```

This is the defect with teeth: the *novel* content of the source (ownership determined by IP
allocation, and the counter-intuitive "Google-owned asset inside a customer block is still
unauthorized") is absent from the admitted entry, while the *already-known* content is what the entry
and the frontier row record. The admission, as landed, buys a vendor instance of F03/F09/F13/F01 and
not the practice that would justify a new frontier row.

## 3. Counterexample — the lane's own admission bar (QUALITY Q5) fails for F26 and only for F26

`corpus/QUALITY.md:18` (Q5): "States at least one falsifiable rule a reader can check against a report
or package, **and at least one rejected over-generalization with its reason.**"

Measured over every entry cited by an admitted frontier row:

```
$ python3 - <<'EOF'
import re
rows=[l for l in open('corpus/README.md') if re.match(r'^\| F\d+ \| .* \| admitted \|',l)]
for l in rows:
    c=[x.strip() for x in l.strip().strip('|').split('|')]
    for e in re.findall(r'knowledge/[a-z0-9-]+\.md',c[3]):
        if not re.search(r'reject',open('corpus/'+e).read(),re.I): print(c[0],e)
EOF
admitted rows 26
F26 knowledge/google-cloud-vrp-customer-resource-boundary.md
```

25 of 25 pre-existing admitted entries contain a rejection statement (the script's test is the
case-insensitive token `reject`): F16's named form at
`knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:210-214` ("**"Registrable on a platform
means its authorization authorizes testing anywhere."** Rejected. …"), the RFC entry's at
`knowledge/rfc-9116-security-txt.md:47` ("Two rejected over-generalizations follow — …"). The F26
entry carries none: `grep -cniE 'reject|over-general|overgenerali'
corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` → `0`. Its `## Limits` (`:20-22`)
states scope limits (a Q4 attribution move), not a named rejected proposition with a reason.

Consequence: the appended claim "26/26 admitted" (`corpus/README.md:630`) overstates the admission bar
by exactly one row. No instrument enforces Q5 (`grep -rlniE 'Q5|rejected over-generali'
corpus/instruments/*.py corpus/instruments/*.sh` → no hits), so this is a human-bar defect, not a
failing gate — which is why it must be caught by a seat, not by a counter.

## 4. Counterexample — the frozen C2 counter is novelty-blind *and* unsatisfiable; three regexes exist for one predicate

`.ufo/waves/round-44/claims.json:23` names this counter:

```
grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md
```

Measured:

```
$ grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md
0                                   # rc=1
$ git show HEAD:corpus/README.md | grep -cE '^\| F[0-9]+ \| admitted \|'
0
```

The status is the *third* cell, so this regex can never match a row — the frozen counter cannot print
25 before or 26 after. The control's own line (`controls/do-nothing.txt:10`), run verbatim as written
in the file (double backslashes), degenerates into an alternation:

```
$ grep -cE '^\\| F[0-9]+ \\| .* \\| admitted \\|' corpus/README.md
631
```

while the figure the control records is 25. Only a third form — single backslashes *with* `.*` —
reproduces the claim:

```
$ grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md
26                                  # 25 at HEAD
```

Three spellings, two wrong, and the wrong ones are the frozen artifacts. This is R22 ("a frozen claim
predicate is checked for satisfiability against base bytes before freeze", `corpus/QUALITY.md:226`)
failed at freeze, and it is also why novelty is unmeasured: a counter over row shape cannot tell a
duplicate F26 from a novel one — both print 26.

## 5. Minor — S069 is an id already used by a different document in the lane's lessons

`grep -rl 'S069' corpus/lessons/` → 10 files at HEAD; those lessons use `S069` for an external
`absent-defect-register` PDF (1,470,121 B, `6.3.1 技术分级` at `S069.txt:1019`,
`corpus/lessons/round-35.md:124,136-137`; `corpus/lessons/round-29.md:146,152,156`). The round-44 row
reuses the token for a 45,681 B JSON capture (`corpus/SOURCES.md:75`,
`corpus/source-snapshots/round-44/S069.txt`). Precedent tolerates id reuse across candidate namespaces
(S068 was a rejected Cisco candidate at round 35 and the GHSA advisory row at round 43), so I do not
call this false provenance — but an unqualified `S069.txt:1019` in a lesson and `S069.txt:61-62` in a
round-44 entry now name two different documents. One disambiguating clause ("lane registry id; distinct
from the round-24–37 external register's S069") closes it.

## Do-nothing discrimination

Measured at HEAD, i.e. the frozen base, not merely asserted:

```
$ git show HEAD:corpus/README.md | grep -c '^| F26'                 → 0
$ git show HEAD:corpus/README.md | grep -cE '^\| F[0-9]+ \| .* \| admitted \|'  → 25
$ git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' → 68
$ git show HEAD:corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md → fatal: exists on disk, but not in 'HEAD'
$ find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l            → 63 (62 at HEAD)
```

A do-nothing replay cannot produce F26, the S069 row, or the entry. **My finding does not falsify C2's
absence premise** — it falsifies the *novelty* of what was landed, which the claim never tests. The
`kill_rule` clause "no coverage credit unless F26, its captured source, knowledge entry and registry
row all land" is satisfied on presence and silent on duplication; that silence is the hole.

## What I checked and did *not* find defective (no verdict inflation)

- Source-row novelty at the registry level holds: the S069 URL appears once in `corpus/SOURCES.md`
  (`grep -n 'bughunters' corpus/SOURCES.md` → S069 and S070 only), so this is **not** the S068/S040
  "adoption would double-register one document" reject shape
  (`corpus/lessons/round-35-verifier-spotcheck.md:107`).
- Tier and opening are as claimed: S069 is `docs`, tier `A`, `mined`, opened 2026-10-28
  (`corpus/SOURCES.md:75`).
- Q1/Q3/Q4/Q6 appear satisfied on inspection: three header lines present (`:3-5`); quote word counts
  13/12/18 ≤ 25; attribution kept ("not a rule for Google's other programs", `:9`); documentation-only
  (`:22`). The entry's own recheck runs and resolves all three anchors:
  `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069`
  → `S069:sha256 OK`, `Q1 OK occurrences=1 anchor=61-ok`, `Q2 OK … 62-ok`, `Q3 OK … 70-ok`, rc=0.
- The frozen census clause holds in the current tree:
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
  → `kasegi ok …/corpus/SOURCES.md`, rc=0 (W04 warnings only for the pre-existing S028/S029 pair).
- Capture↔row binding holds **now**, after an in-flight manifest edit at 16:05:14 local: the record
  carries `url` (registry URL) + `capture_url`/`http.final_url` (the `/rest/v1/articles/…` endpoint the
  bytes actually came from) and
  `python3 corpus/instruments/capture-binding-check.py --root .` → `round-44 records=1 url_bound=1`,
  `records=58 bound=58 unbound=0`, rc=0. **Recorded transient:** the same run on the pre-edit tree
  printed `MANIFEST round-44 records=1 url_bound=0` and
  `FAIL rule=url-mismatch record=S069 row=S069 dir=round-44`, `records=58 bound=57 unbound=1` (B5,
  `corpus/instruments/capture-binding-check.py:52-55`). I report both states; the earlier FAIL line's
  exit status was not captured (piped), so I do not claim it.

## Impacted axes

- `coverage` (C2) — the primary hit: the row is reachable but carries no new practice; the one novel
  rule is a sub-clause and the best novel rule is missing. Credit should be restated, not enlarged.
- `depth:verifiability` — the claim's own counter is unsatisfiable and the control's is not
  reproducible as written (§4); a C2 pass printed from either would be unbacked.
- Admission-bar integrity (`QUALITY.md:18` Q5) — one row, fixable in one paragraph.

## Smallest safe correction (in order of cost)

1. **Restate F26's ground to the one absent rule.** Make `corpus/README.md:628`'s `next` cell name the
   tenant/isolated-environment rule and, preferably, the customer-IP-range rule
   (`S069.txt:73-77`), and add a one-line novelty diff to the entry naming F03:8, F09:46, F13:16,
   F01:34 and the S020/DOJ entry as rules it *shares* rather than opens. No new source, no new row
   count change; the frontier stays 26.
2. **Add the Q5 rejection** to the entry — e.g. reject "a Google-owned asset inside a customer IP block
   is in scope" with `S069.txt:76-77` as its reason. This is the same edit that records the novelty,
   and it makes "26/26 admitted" true.
3. **Fix the counter before citing it.** Land the R22 erratum: use
   `grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md` (25→26) and record the control's
   double-backslash spelling and its 631 result as the superseded literal. Do not report 26 from
   `claims.json:23`.
4. **Add the S069 namespace clause** (§5) to the row or the round-44 lesson.
5. **Do not credit the recorded reject as a novelty check.** S070 (`corpus/SOURCES.md:76`) is a
   JavaScript shell — it exercises "is this page operative text", not "is this practice already
   admitted". The lane's own novelty reject precedent is the duplicate-document form
   (`round-35-verifier-spotcheck.md:107`); if a reject is meant to carry taste, it should be of that
   shape. This is an observation about discriminating power, not a claim that C2's "recorded reject"
   clause fails.

## Limitations

- I read the working tree, which is being edited live by the integrating L1: the F26 row, S069/S070
  rows, the entry and the manifest are **uncommitted** at HEAD. Line numbers are current as of
  2026-10-28T19:14Z and may move on integration; the base-state numbers (§Do-nothing) are from
  `git show HEAD:` and are stable.
- My novelty comparison covers the corpus prose surfaces (`corpus/knowledge`, `corpus/README.md`,
  `SKILL.md`, `corpus/PROVINCE.md`, `corpus/QUALITY.md`) and the registry. It does not sweep the
  `.ufo/` wave receipts of earlier rounds as authorities, and it does not open the network to test
  whether Google's page has changed since `2026-10-28T18:53:38Z`.
- Q1/Q3/Q4/Q6 were checked by inspection plus the entry's own recheck run; no Q-instrument exists, so
  that check is mine, not a gate.
- I did not run any gate owned by another seat (`r44-routed-defects.py` does not exist yet), did not
  execute `sources-census.sh` beyond the read-only `validate` subcommand, and made no edit outside this
  report.
- Scratch: `HYAKU_SCRATCH` is unset in this session; `mkdir -p "${HYAKU_SCRATCH:-/nonexistent}/kasegi-r44/R44Critic11"`
  → `Permission denied` (rc=1). No scratch workspace was created. Disclosure: one transient redirect
  (`python3 corpus/instruments/capture-binding-check.py --root . > /tmp/x`) was used to read an exit
  status and removed immediately (`rm -f /tmp/x`); it was a pipe target, not a scratch tree, but it is
  outside the spec's named scratch location and I record it rather than omit it. No other file was
  written outside this report.
- Tools: none installed or upgraded; `/home/vgpnk/.omp/agent/RULES.md` read first, no install
  performed, no pacman invoked.
