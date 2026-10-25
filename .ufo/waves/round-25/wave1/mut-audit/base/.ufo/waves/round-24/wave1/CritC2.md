# CritC2 — C2 (coverage) falsification, round 24

Seat: critic (read-only). Base claims: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/claims.json`
(`base d0a3f6a…`, lane master at `c2480b143120364728b40397926ffcf30a7309c8`, base is its parent).
Nothing below edits the lane; every command was run read-only from the lane root or from `/tmp/critc2`.

**Verdict.** C2 as frozen is **not a coverage-axis move**: under the lane's own coverage
definition and its two recorded precedents it is bookkeeping plus (at best) one capability.
Two of its three supporting devices are broken: **counter B does not measure its predicate**
(false green and false red both demonstrated), and **the word "addendum 10" resolves nowhere**.
Adopted as written it **harms depth:verifiability** by adding Frontier entries that the C1
counter cannot see and whose rechecks exit 2. The substantive gap C2 wants to fill is real,
so the correction is small: re-scope the claim, fix the counter, and either capture the new
rows or refuse the entries under C2's own kill rule.

---

## F1 — counter B counts an id band, not "first registered this round" (blocks the claim)

`command_B`: `grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l`, target `2`.
Receipts at base: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` claim reproduced —
`0` at base (matches `before_expected_B`), `awk` counter A = `8` (matches `before_expected_A`).

The counter's four failure modes, all measured on fixtures in `/tmp/critc2/knowledge/`:

| case | fixture | grep count | truth |
|---|---|---|---|
| predicate MET, dense next ids `S032/S033` (the order `staged-ids` stages) | `e1.md`,`e2.md`,`e3.md` | **0** | 3 entries from rows first registered this round → **false red** |
| predicate NOT met, rows already numbered `S100/S101` cited | `old1.md`,`old2.md` | **2** | nothing registered this round → **false green, target met** |
| multi-id `source:` lines (`S120, S121` / `S122-S123`) | `e4.md`,`e5.md` | **0** (not in the 2) | predicate met → **false red** |

- The pattern requires a literal space directly after the third digit, so `S120,` and `S122-S123`
  are invisible; `grep -l` also counts **files**, and never checks `status`, `opened`, or `used-by`
  in `corpus/SOURCES.md`.
- Id sequence of record: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/assimilation/staged-ids`
  stages `S031` … `S124` **in dense order** (94 ids, `S032` immediately after `S031`, `S100` at
  line 70). Two adopted entries assigned in that order land on `S032`/`S033` → **counter B stays 0
  while the predicate is satisfied**. Reaching `2` requires either assigning ids out of staged order
  or picking the `S100+` tail on purpose — i.e. shaping the artifact to satisfy the counter.
- `corpus/SOURCES.md` today holds exactly `S001`–`S031` (`grep -oE '\bS[0-9]{3}\b' corpus/SOURCES.md | sort -u`),
  so there is no pre-existing `S1xx` row *yet*; the false green appears the moment the staged
  `S100`–`S124` block lands (any entry citing one of those rows counts, whatever its provenance).
- This is the r23 erratum's own lesson repeating in the opposite direction: the r23 fix replaced a
  column-agnostic `grep -cE` with a column-aware `awk` for counter A, while counter B stays a
  filename/prefix heuristic.

**Smallest safe correction.** Freeze the two entry filenames and their expected row ids in the claim
(r23 named F06–F08 and S018/S030/S029 explicitly), and replace counter B with a row join on
`corpus/SOURCES.md`: count entries whose first `source:` id has a row with `status=mined`,
`opened=<round date>`, and `used-by` pointing at that file.

## F2 — C2 as frozen regresses depth:verifiability through C1's 8-name enumeration (blocks the claim)

- C1's predicate: "every one of the **eight** Frontier knowledge entries runs its own `recheck:`
  command and exits 0" — `claims.json` C1. Its `counter_A` hardcodes eight filenames.
- C2 adds **two more** Frontier entries (`F09`), so after C2 the frontier entry set is **10**
  (`ls corpus/knowledge/*.md | wc -l` = 33 today; `grep -cE '^\| F[0-9]+ .*\| admitted \|' corpus/README.md` = 8).
  C1 can then land "8/8 exit 0" while `README.md` advertises 9 admitted topics / 10 entries, two of
  which were never run. That is the F01–F05 defect (the exact thing C1 exists to cure) re-created
  under the other claim — a **masked depth regression**.
- Measured, the new entries would in fact fail: the only lane instrument is
  `corpus/instruments/source-recheck.py` against
  `corpus/source-snapshots/round-23/manifest.json`, whose sources are exactly
  `S018 S029 S030 S031` (`grep -oE 'S0[0-9]{2}' …/manifest.json | sort -u`). A new row is not listed:
  `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S123`
  → `S123:source UNAVAILABLE reason=not-listed`, `exit=2`.
- C2's `surface_changed` names only "Frontier topic set". A round-24 capture store + manifest entry
  for the new rows is therefore **undeclared and unmeasured** — but is the only way the new entries'
  rechecks can exit 0. The claim is internally in tension: satisfy the predicate → add an undeclared
  capture surface; do not → the entries fail C1's instrument and must be refused under C2's kill rule.

**Smallest safe correction.** Either (a) extend C2's surface to "frontier topic set **and** a
round-24 captured-source manifest covering the new rows", and extend C1's counter A to 10 named
entries; or (b) refuse both entries this round and let C2 land short (the claim already authorises
that as honest stop). Do not land entries whose recheck is not in a manifest.

## F3 — "new frontier topic admitted" is bookkeeping against the adopted coverage metric

Definition of record, `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md:43`:
"**coverage** — top-level surfaces of the domain root that have either (a) a corpus entry documenting
a full census/full read, or (b) a recorded park disposition."
`corpus/README.md:209` says of the frontier: "the public-practice frontier above is a separate
denominator (8/8 admitted at round 23) and is not counted into the 0/18 figure."

Precedents in the same file:
- r22: "Frontier topics admitted **0/5 → 5/5** … **Score held**: the r15 domain-root definition is
  unchanged by public-practice entries (**r22 critic**)", with the 20+5 denominator only
  "*proposed* for adoption next round".
- r23: "F06–F08 admitted **0/3**; frontier **8/8** … **Improved, score held 7**."

So a critic has already ruled this exact mechanism non-creditable, twice. No round has adopted the
proposed 20+5 denominator, and `claims.json` C2 does not declare a denominator change — it simply
sets `after_target_A: 9` and `target_axis_or_capability: "axis"` with `axis_score_before: 7`.
A count inside an unadopted proxy is not the coverage score.

What is genuinely new is the **capability**: statutory/engagement-document authorisation analysis
(the r22 `sources-registry` pattern — new capability, score held). C2 should be reclassified that
way, or the denominator adoption must be frozen in `claims.json` *before* the move and recorded in
`SCORECARD.md` the way r22 recorded the PROVINCE Core/Frontier/Adjacent classification.

Command A itself is sound and reproduces: `8` at base, and it is the column-aware `awk` the r23
erratum asked for. It measures the table, not the substance: a README row plus two one-line files
satisfies both counters with no re-opened row and no quote.

## F4 — "the lane holds neither an engagement document and a statute" is false in its second conjunct

C2 `surface_changed`: "The lane holds neither: `grep -riE 'rules of engagement|statutory authorization' SKILL.md corpus/knowledge/` counts 0 hits at base."
The grep reproduces (`0`), but it is scoped to two phrases, not to the concept:

- **Engagement-document limb — genuinely unheld.** `grep -rilE '800-115|rules of engagement' SKILL.md corpus/ PROVINCE.md`
  → **no files**. The nearest held material is program *policy* text: F03's Rule
  (`corpus/knowledge/authorization-safe-harbor-and-scope.md` §Rule) and `SKILL.md:1021`
  ("Check its actual asset scope, testing grant, and prohibited methods separately"). Those govern a
  platform's policy, not a pre-engagement authorisation instrument. No duplicate authority here.
- **Statutory limb — partially held.** `corpus/SOURCES.md` already carries a statute at tier A:
  `S024` ("Regulation (EU) 2024/2847, Cyber Resilience Act", `queued`) and `S029`
  ("CRA manufacturer reporting clocks", `mined`, `used-by corpus/knowledge/cra-manufacturer-reporting-duties.md`).
  The lane therefore holds a statute; what it does not hold is a statute that **defines
  authorisation**. Also, F03's §Limits literally names the gap C2 fills: "These sources do not
  resolve third-party asset ownership, external legal protection, or whether an unlisted activity is
  authorized in a particular jurisdiction." That sentence is evidence FOR the gap and against the
  claim's wording, simultaneously.
- Related. `grep -ricE 'authori[sz]ation|authori[sz]ed'` at base: `SKILL.md:9`,
  `authorization-safe-harbor-and-scope.md:9`, `policy-access-playbook.md:3`, `triage-thresholds.md:2`,
  `cra-manufacturer-reporting-duties.md:2`, `multiparty-vulnerability-coordination.md:2`, etc. The
  concept is present; the *instruments* are not.

**Smallest safe correction.** Replace with: "the lane holds neither a rules-of-engagement document
nor a statute that defines authorisation; its only statute (CRA, S029/S024) sets manufacturer
reporting duties." Keep F03 as the parent topic and require F09's row to declare the extension
(F03's own `next` cell: "Attribute protections to the policy that grants them; do not generalize").

## F5 — both candidate entries, taken verbatim, fail the lane's own Q1/Q3/Q7 gates

Package: `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/`.

- **Q1 (headers under an H1) — RoE entry fails.** `head -6 authorised-testing-rules-of-engagement.md`
  shows a blank line 1 then `source:` at line 2; `grep -c '^# ' …` = **0**. No H1 title at all.
  No lane entry lacks one: `for f in corpus/knowledge/*.md; do grep -c '^# ' "$f"; done | sort | uniq -c`
  → `30 × 1`, `3 × 2`, `0 × 0` over 33 files.
- **Q7 (recheck is a command, not prose) — both fail, measured.**
  Rechecks as filed: `recheck: 90d — re-fetch the PDF and \`grep -F\` the four lines (ran 2026-10-24)`;
  `recheck: 730d — \`curl -sSL https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128\` then confirm 第十一条 still reads … (ran 2026-10-23)`.
  Run exactly as C1's loop runs them (`r=$(grep -m1 '^recheck: ' … | sed 's/^recheck: //'); bash -c "$r"`),
  **both exit 2** with `bash: -c: line 1: syntax error near unexpected token '('`. A bare cadence
  passes cleanly as "not-listed" (`bash -c '90d -- x'` → `90d: command not found`, exit 127).
  Note the ambiguity this exposes in C1: **exit 2 is not a unique signal** — it is produced both by
  `source UNAVAILABLE reason=not-listed` and by a bash syntax error, so "exit 2" cannot distinguish
  "no capture" from "unparseable prose". C1 should print the reason string, not only the code.
- **Q3/Q4 — the RoE entry smuggles four uncited legal assertions.** Lines 33–34:
  "the procuratorate's 合法授权不等于无限授权, the 静安 case, the 指导案例145号 line".
  S-ids anywhere in that entry: `S123` only (`grep -oE 'S[0-9]{3}' | sort -u` → `S123`);
  `grep -n '静安\|145号\|procuratorate\|合法授权' | grep -c 'S[0-9][0-9][0-9]'` → **0**. These are
  load-bearing in §Kasegi use and carry no quote, no location, no row. Q3 requires a verbatim quote
  ≤25 words with location per load-bearing claim; Q4 requires attribution. The lane refuses the
  package's Chinese entry (`candidate_refuse`), so it has **no row to cite** for them.
- **Q4/Q5 — statutory entry title overclaims.** Title "Statutory authorization in three traditions";
  body: "The **Chinese** half of the three-tradition comparison is not covered". One tradition is
  documented, the western half lives in the *other* entry. Retitle or drop the count.
- **False provenance if copied.** `verified-at: 2026-10-24` / `2026-10-23` are the package author's
  re-open dates. Round 24 is 2026-10-25 (`claims.json frozen_at_utc`); Q1 requires the admitting
  author's own date. Copying either is a provenance misstatement, and the honest alternative
  (`verified-at: 2026-10-25`) obliges an actual re-open plus capture — see F2.
- **Q2 tier** is satisfiable: NIST SP 800-115 and the e-Gov consolidated statute are official
  tier-A documents. Flag only the 2008 date of the NIST guide (entry already says "the version NIST
  still serves"); its `Limits` correctly refuse to present it as law. **Q6 survives**: neither entry
  instructs probing, both cite public documents, no credentials/session/private URL; the RoE entry's
  "A tester who stays inside the ROE is exercising the authority the ROE grants" is descriptive of
  NIST's clause (keep it attributed).

## F6 — the predicate's normative referent does not exist

- `grep -rn "addendum 10\|Addendum 10\|addendum-10\|addendum #10"` across
  `/home/vgpnk/Projects/shokunin` (excluding the claims file itself) and
  `/home/vgpnk/Projects/shokuknow/merge/kasegi` → **0 hits**. `corpus/QUALITY.md` has no addendum
  section (`grep -n 'addendum' corpus/QUALITY.md` → 0); `corpus/SOURCES.md` contract v1 has none.
  The predicate "rows first registered this round **under addendum 10**" therefore has no rule a
  reader can apply. (UNVERIFIED whether an addendum 10 exists outside both repos; blocked by scope —
  only these two roots are readable, and it is not in either.)
- `claims.json` → `assimilation.collision_map` =
  `.ufo/waves/round-24/assimilation/renumber-map.tsv` is **absent**
  (`test -e` → exit 1; the directory holds only `census-before.txt`, `collisions`, `reg-ids`,
  `staged-ids`). A frozen claim pointing at a non-existent map is not re-derivable from committed bytes.
- The RoE entry's `ground: round-15 ledger item 2` and the statutory entry's `ground: F12 (new
  frontier item …)` are **package-internal ids**. The lane's frontier stops at F08; `F12` must be
  renumbered to `F09` on adoption or it becomes a phantom pointer / future-id collision.

## F7 — adopting F09 leaves two stale self-descriptions, neither in the counter set

- `corpus/README.md:209`: "public-practice frontier above is a separate denominator (**8/8 admitted
  at round 23**)".
- `PROVINCE.md:38`: "indexed in corpus/README.md under Frontier **F01–F08**".
C2's counters are `awk`-on-F-rows and the `S1xx` grep; neither reads these two sentences, so the
lane can claim F09 while both files state the old range. R2 ("self-description is a claim") applies;
r22 measured PROVINCE explicitly. Add a `grep -c 'F01–F09' PROVINCE.md`-style command or update both
in the same commit.

## F8 — adjacency / re-scope risk (reported, not scored)

The statutory candidate is Japanese criminal law (不正アクセス法, 平成11年法律第128号). PROVINCE
Core covers "program rules, scopes, and claim packages"; `PROVINCE.md` refuses out-of-domain material
and records that "the lane did not re-scope itself" — re-scope is the operator's. Admit the entry as
**scope/authorisation** (access-manager consent = scope owner) and keep the entry's own honest limit
(Chinese half uncovered, no substitution). If a later round absorbs the package's Chinese criminal
corpus, that is a province change needing an operator decision, not a coverage gain.

---

## What would make me call C2 harmed (the trigger list)

1. `after_target_B` recorded as 2 while the two cited ids are outside the round's registration — or
   while no round-24 manifest entry exists for them (F1, F2).
2. Two new Frontier entries land and C1 is filed as "8/8": the honest ratio becomes 8/10 (F2).
3. The RoE paragraph naming 静安 / 指导案例145号 lands with no row and no "not re-opened" marker (F5).
4. `verified-at: 2026-10-24/23` copied from the package, or the package's prose recheck copied
   verbatim (F5).
5. `coverage` recorded as 7 → 8 in `SCORECARD.md` without a denominator adopted in the same frozen
   claim (F3).
6. `F12`, `S123`, `S039–S041` or `addendum 10` left as live references (F6).

None of 1–6 is unavoidable. C2's own kill rule ("refusals are evidence, not padding") already
authorises landing short, which is the honest stop if the entries cannot be re-grounded to the lane's
capture instrument this round.

## Axis impact summary

| axis | effect as frozen | evidence |
|---|---|---|
| depth:verifiability | **harmed** (2 new entries outside C1's enumeration; rechecks exit 2) | F2, F5 |
| coverage | **not moved** (unadopted denominator; r22+r23 held) | F3 |
| depth:density | untouched (no SKILL/corpus block change declared) | — |
| Q2 tier | satisfiable if rows are re-opened this round | F5 |
| Q4 attribution | **harmed** as drafted (uncited Chinese assertions; one-tradition title) | F5 |
| Q6 documentation-only | survives; no probing, no credential material | F5 |

## Installs / side effects

No tool installed, upgraded or removed; no PACMAN invocation. Writes: this report only
(`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/wave1/CritC2.md`) plus throwaway
fixtures under `/tmp/critc2/`. Lane tree, git/jj state, `/home/vgpnk/Projects/shokuknow` untouched.
