# Round 25 wave 1 — is F10 ground the lane did NOT hold?

Seat: `L1Kasegi25.CritC2Ground` (critic, READ-ONLY). Lane base
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. No production edit, no file outside this one
written, no tool installed or upgraded. Every number below was produced by this seat against
the lane tree as it stood at read time (wave 1 is concurrent: the F10 entry and the
`round-25/` captures appeared while this seat was reading, and are marked as such).

## Verdict

**`new ground`** — with two overlaps that must be named in the entry and the report, not
suppressed. No tracked entry at the lane base documents a vendor's own published policy about
handling reports of its own products.

Vehicle of record at read time is the **lane-native** entry
`corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` (untracked, `ground: F10`,
header ids **S036–S039**, capture-anchored quotes, FR-1…FR-4, four rejected
over-generalizations). It is **not** the merge-package file
`japanese-vendor-disclosure-policies-2026-10-23.md`, which declares `ground: F09` and whose
recheck cannot pass C1 (see §4.2). Two vehicles for the same four captures would be duplicate
authority; only the lane-native one should land.

## 1. Does any existing entry already hold a vendor's own published policy?

No. Measured at the lane base:

| probe | command | observed |
|---|---|---|
| vendor names in tracked corpus + skill | `git grep -niE 'cisco\|cybozu\|pepabo\|hitachi' b49948f -- corpus/knowledge SKILL.md \| wc -l` | **0** (all 22 hits in the tree today are inside the untracked round-25 entry) |
| ISO/IEC 29147 as a corpus object | `git grep -n 'ISO/IEC 29147' b49948f -- corpus/` | **2 hits, neither ground**: `corpus/SOURCES.md:63`, under `## Leads (unopened)` — "ISO/IEC 29147 vulnerability-disclosure and ISO/IEC 30111 vulnerability-handling standard records at https://www.iso.org/standard/72311.html"; and `corpus/source-snapshots/round-23/S018.txt:3` — FIRST v1.1's own sentence "Definitions that are available in ISO/IEC 29147:2014 are used with minimal modification", a capture of a *reference*, not the standard's content |
| lifecycle / PSIRT ground | `git grep -niE 'LDoS\|Last Day of Support\|coordination partner\|PSIRT' b49948f -- corpus/knowledge SKILL.md \| wc -l` | **0** |
| frontier row | `grep -c '^\| F10' corpus/README.md` | **0** (F01–F09 only) |

What the four surfaces the assignment named actually hold:

- `corpus/knowledge/program-quirks.md:16-56` — **programme** quirks, platform by platform:
  Cantina `$100` deposit, vulnerable-pattern OOS, SEAL Whitehat = active exploits only;
  HackerOne React-controlled portal fields and GraphQL `team(handle)`; Intigriti
  self-assigned severity; Bugcrowd SEEK identity + AI-content clauses. Every row is a rule a
  *programme* imposes on a reporter. None is a vendor's process, standard alignment,
  coordination partner or acceleration condition.
- `corpus/knowledge/authorization-safe-harbor-and-scope.md:11-24` — S006 HackerOne
  safe-harbor FAQ, S007 Disclose.io/Bugcrowd commitment, S008 CISA agency template. Platform
  model + government template. Its own rule ("identify the actual program policy, not only
  the platform summary") *points at* a vendor policy but holds none.
- `corpus/knowledge/coordinated-disclosure-timelines.md:22,24-25` — the closest form match:
  S004 CERT/CC "45 days after the initial report" and S005 Project Zero "90 days … 30 days
  after the fix was made available … 14-day grace extension". Two published third-party
  policy statements with a trigger, an interval and an exception.
- `corpus/knowledge/vdp-disclosure-packages.md:13,23-24` — one observed vendor intake route
  (Anthropic `security.txt` Contact → H1 `embedded_submissions`), recorded as a
  claim-package shape and anchored to a lost tree. No policy text.
- `corpus/knowledge/multiparty-vulnerability-coordination.md:25-29` — FIRST v1.1 roles
  (coordinator / upstream / downstream vendor). An industry guideline about roles, not a
  named vendor's own policy.
- `corpus/knowledge/policy-access-playbook.md:9-12` — how to *fetch* a platform policy
  (GraphQL vs SPA, `security.txt` stub ≠ scope). Retrieval, not content.

The F10 object set — intake-channel list, handling scope vs disclosure scope as two lists, a
borrowed severity instrument, a negotiated publication date, coordination partners, a
lifecycle boundary, a conditional non-litigation statement — appears in none of them.

## 2. Is "vendor policy" distinct from programme rules and from F03/F09?

Distinct, on the party and on the object:

| kind | who publishes | what it states | lane surface |
|---|---|---|---|
| programme rules | platform / programme owner (H1, Bugcrowd, Cantina) | what the programme offers and forbids a reporter: scope list, reward ladder, submission form, platform safe-harbor model | `program-quirks.md`, F03 |
| F03 safe harbour | platform docs + a government template | the *model* of safe harbour and the warning that a badge adds no scope | `authorization-safe-harbor-and-scope.md:11-24` |
| F09 engagement / statute | NIST, e-Gov, NPA | the instrument that authorises **one engagement** (ROE + exclude list) or the statutory definition of unauthorised access | `authorised-testing-rules-of-engagement.md`, `statutory-authorization-and-unauthorized-access.md` |
| **F10 vendor policy** | the vendor, about its own products | standing process: intake channels, handling vs disclosure scope, severity instrument, publication portal/timing, coordination partners, lifecycle boundary, protection statement | new |

Exact overlaps to name, not hide:

1. **F02 form overlap.** S004/S005 already show a *published, attributed policy statement with
   a trigger and an exception*. What they are not: a product vendor's handling policy. CERT/CC
   is a coordinator; Project Zero's clock governs disclosure of *other* vendors' unfixed bugs.
   Neither has intake scope, product scope, ISO alignment, coordination partners or a
   lifecycle boundary. Overlap = form (policy-as-object), not kind.
2. **F03 content overlap.** A vendor policy can carry a safe-harbour statement — Pepabo
   `S038.txt:17` "条件を守る限りにおいて、…法的措置をとらない方針です". That is the vendor-level
   instance of F03's concept and must be attributed as that vendor's *conditional* position
   (Q4), with the prohibition list `S038.txt:24-25` beside it. The concurrent entry's rejected
   over-generalization #3 already draws this line correctly.
3. **F09 boundary.** A vendor's published policy is neither a case-specific ROE nor a statute.
   Pepabo's page is the nearest thing to an authorisation document, and it is explicitly
   conditional; treating it as F09 ground would repeat the lane's A7 anti-pattern.

So: new ground on kind, overlapping on form (F02) and on one content limb (F03).

## 3. Breadth or depth — and does the coverage axis allow breadth?

It is **breadth by construction**: a surface not previously governed, not a deeper read of one
already governed. The axis permits it, because breadth of real surfaces *is* the definition:

- `AXES.md:12` — "| **coverage** | Fraction of the domain's real surfaces the skill governs
  (repo paths, tools, edge classes) | PROVINCE.md lists every surface; none unexplored without
  reason |"
- `AXES.md:21` — "Expansion ↔ `coverage` + `adjacency`".

Two constraints the lane's own record adds on top:

- The SCORECARD proxy requires "a corpus entry documenting a full census/full read" — met here:
  four pages read as pinned captures, with per-claim quotes and line anchors.
- The frontier denominator is **self-declared and grows with the numerator**: r22 proposed
  "(20+0)/25 → (20+5)/25", r23 "frozen at eight topics: 5/8 → 8/8", r24 "8 → 9" — and the
  coverage score stayed **7** through all three. The C2 counter (`frontier admitted = 10`) is
  numerator-only; admitting F10 raises the declared set at the same time. Therefore this is
  legitimate coverage *work* and an expansion gain, but **not a score move**: the cell is
  `coverage 7 held`. Reporting it as an improvement would be the premature-saturation error.

## 4. Counterexamples this seat measured (impacted axes)

### 4.1 C1's frozen target `lines=35` is arithmetically incompatible with C2's vehicle

`corpus/instruments/recheck-audit.py` emits `"lines": len(entries)`, and `collect()` yields one
record per `corpus/knowledge/*.md` that has a `recheck:` line. Today
`grep -c '^recheck:' corpus/knowledge/*.md | awk -F: '{s+=$2} END{print s}'` → **35**, matching
the frozen `lines=35`. Landing the F10 entry makes it **36**. C1's frozen target string
`lines=35 pass=35 exit=0` then cannot be printed by any tree that also satisfies C2.

*Impact:* depth:verifiability (C1). *Correction:* report C1 as `lines=36 pass=36 exit=0` and
name `lines=35` as the pre-admission count, or measure C1 before the entry lands and disclose
the change; do not publish `lines=35` after the entry exists.

### 4.2 The F10 entry's recheck names a manifest that does not exist yet

`vendor-disclosure-policies-as-corpus-objects.md` `recheck:` parses (`bash -n` → 0) and is
cwd-pinned, but names `corpus/source-snapshots/round-25/manifest.json`, and
`test -e` → **ABSENT** (the directory holds `S036.txt … S040.txt` only). The audit's limb (c)
is path existence, not fail-closed execution: `missing_paths` is non-empty → the line FAILS,
so `pass` stays 6 of 36 and the harness prints `manifest-unreadable`.

*Impact:* depth:verifiability (C1), coverage (C2 census/recheck). *Correction:* write
`round-25/manifest.json` before the C1 after-receipt is taken, then re-run
`python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-25/c1-after.json` and
`python3 corpus/instruments/frontier-recheck-count.py`.

### 4.3 The merge-package vehicle is a regression, not an alternative

`japanese-vendor-disclosure-policies-2026-10-23.md` (staged) has
`recheck: 180d — \`curl -sSL https://cybozu.co.jp/company/security-policy/\` then confirm … (ran
2026-10-23)`: `bash -n` → **exit 2** (`syntax error near unexpected token '('`), and
`CORPUS_PATH_RE`/`HOME_BASE_RE` → **0 tokens** of either kind, so it fails C1 limbs (a) and
(c), Q7, and R12/harness condition C (not a `source-recheck.py` invocation). Its `ground:` line
says **F09**, not F10. If it is named as the F10 row's entry, `frontier-recheck-count.py`
prints `entries=11 pass=10 exit=1` (each admitted row's entry is evaluated; conditions A–D fail
at "not-a-recheck-invocation"), regressing the round-24 capability receipt (10/10 exit 0,
re-measured by this seat).

*Impact:* depth:verifiability, operability (recorded capability). *Correction:* land the
lane-native entry only; if the staged text is reused, re-ground its `ground:` line to F10 and
replace its recheck with the manifest-bound form.

### 4.4 Appending the merge package's rows would trip the census's own duplicate-URL error

Round 25 allocated **S036=Cybozu policy, S037=Cybozu FAQ, S038=Pepabo, S039=Hitachi**
(`.ufo/waves/round-25/capture-log.txt`; the staged package numbers the same four pages
S055/S056/S057/S060 — identical URLs, same `docs` scope). `scripts/sources-census.sh:641-649`
raises **E04 "duplicate url within scope"** (an error; W04 is only the cross-scope warning), and
the census today is exit 0 with `rows 35`. Appending both id sets puts two `docs` rows on each
of the four URLs → E04 → non-zero exit → C2's own predicate ("census validates exit 0") fails.

*Impact:* coverage (C2, by its kill rule "a staged row is appended unnormalized").
*Correction:* register the four pages once, at S036–S039, and map the package's S055–S060 to
those ids instead of appending them; append only rows for URLs the lane has not fetched.

### 4.5 The frozen reject premise is falsified by the lane's own capture

`claims.json` assimilation plans to reject `vendor-cvd-policy-crosswalk-2026-10-23.md` because
"S068 Cisco policy unreachable this round". The lane now holds
`corpus/source-snapshots/round-25/S040.txt` (33 KB, untracked), and
`.ufo/waves/round-25/capture-log.txt:14,25,27` records it as
`S040 status=200 fetched_bytes=94027 … utc=2026-10-25T08:14:28Z`, mapped to staged id `S068`,
with the note that "a plain `curl -L` with a browser UA returned http 403 for S040 while the
capture instrument's own [route succeeded]" — i.e. the page is reachable, only the naive
fetch is not. The capture carries ISO/IEC 29147:2018 at `:58`, coordination partners CERT-FI /
JP-CERT at `:188-189`, `Last Day of Support (LDoS)` at `:163`, and the acceleration conditions
at `:301-302`. Those are precisely the two limbs of the F10 definition the admitted JP entry
does not carry (standard alignment, acceleration conditions).

*Impact:* coverage (C2's declared object), calibration. *Correction:* state the reject on its
real ground (the sibling scope seat's Q3 count defect: "the two conditions" vs four situations
at `S040.txt:301,302,305,308`) and do not carry "unreachable" into the report — or admit a
Cisco entry and let F10 hold all four limbs.

## 5. Smallest safe correction set

1. Land `vendor-disclosure-policies-as-corpus-objects.md` as the single F10 vehicle (not the
   merge file), with `ground: F10` as it already reads.
2. Write `corpus/source-snapshots/round-25/manifest.json` before any C1 after-receipt.
3. Add the `F10` row to `corpus/README.md` § Frontier **and** update `PROVINCE.md:38`
   ("Frontier F01–F09 … 9/9 admitted") to F01–F10 / 10/10 in the same commit — r24's verifier
   checked that the README and PROVINCE agree.
4. Register S036–S039 in `corpus/SOURCES.md` once; map the package's S055–S060 to them.
5. Print C1 as `lines=36 pass=36` (35 named as pre-admission) and keep the coverage cell at
   **7 held**.

## 6. The sentence the L1 should put in the report

> F10 is new ground at base `b49948f`: no tracked entry held a vendor's own published
> product-handling policy (0 hits for Cisco/Cybozu/Pepabo/Hitachi; ISO/IEC 29147 appears only
> as an unopened lead at `corpus/SOURCES.md:63` and a one-line cross-reference inside the FIRST
> capture `round-23/S018.txt:3`, never as content), and the object it adds — intake-channel
> list, handling scope vs disclosure scope, borrowed severity instrument, negotiated publication
> date, coordination partners, lifecycle boundary, conditional non-litigation statement — is
> held by no existing entry; it overlaps F02 only in the published-policy *form* (CERT/CC S004,
> Project Zero S005) and F03 only where a vendor policy states its own safe harbour (Pepabo,
> `S038.txt:17`, conditional), both of which the entry attributes rather than generalizes; the
> move is breadth, which `AXES.md:12` defines coverage as, so the honest cell is coverage **7
> held**, expansion improved — not a score move.

## 7. Coordination note (no duplicate authority between critic reports)

`CritC2Scope.md` (sibling seat) already measured the staged rechecks' `bash -n` failure, the
missing round-25 manifest, the absent F10 row, and refused the Cisco crosswalk on its Q3 count
defect. This seat does not re-judge scope, admission, or the reject list; it adds only the
ground verdict, the overlap set, the axis reading, and §4.1/§4.4 — the two interactions the
scope seat did not measure (the `lines=35` arithmetic and the census E04 duplicate-URL error).
