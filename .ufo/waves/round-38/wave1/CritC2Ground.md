# CritC2Ground — is CSAF/VEX genuine uncovered ground for kasegi? (round 38, coverage)

Seat: critic, lane axis `coverage`. Item: attack the F21 admission (OASIS CSAF v2.0 / VEX
profile, source S055). Receipt only — nothing here is landable text.

Reviewed state: base `a173b0c2` + in-flight C2 landing as it stood while this seat ran
(`corpus/SOURCES.md` S055 row at :61, `corpus/knowledge/csaf-vex-product-status-and-justifications.md`,
`corpus/source-snapshots/round-38/{S055.txt,manifest.json}`, `corpus/README.md` F21 row at :477 and
`[r38 amendment]` 21/21 line, `PROVINCE.md:156` `[r38 Frontier amendment]` F21 line). All of it is
uncommitted at the time of writing (`git -C … status --porcelain` shows `M PROVINCE.md`,
`M corpus/README.md`, `M corpus/SOURCES.md`, `?? corpus/knowledge/csaf-vex…`, `?? corpus/source-snapshots/round-38/`).

## Verdict

**The admission holds on the merits.** I could not construct a counterexample that kills it from
local evidence. Six attacks were run; four fail outright, and two fail as *kills* but land as
**record-precision defects** that a canonical Rust judge (or an outside verifier) would still
flag. Those two are listed under "Impacted axes" — neither changes the coverage score, but one of
them becomes a false-provenance kill if the round-38 lesson or report generalises the
uncovered-ground sweep the way earlier rounds generalised similar numbers.

| # | strongest form of the attack | measurement | holds? |
|---|---|---|---|
| A1 | F21 is not new ground: the lane already names CSAF twice in *mined* sources | 4 pre-existing captures mention CSAF/VEX; **0** of them contain the vocabulary F21 claims (`product_status`, `known_not_affected`, `component_not_present`, `VEX-Justification`) | **no** — fails at the vocabulary level, which is the claimed level |
| A2 | Out of province: vendor-side advisory *authoring* is publisher engineering, not bounty/security research | PROVINCE Core names "submission/disclosure packaging"; the reject rule would also reject F01/F07/F08/F11 (specs the researcher reads, never writes) | **no** — over-broad rule; survives only as a framing constraint, which the landed entry satisfies |
| A3 | Contested: kake's security.txt entry already mentions `CSAF` | kake:63 is a field-cardinality bullet citing S079; kake's own scope line disclaims content; no product_status/justification text in kake | **no** — but it installs a real fence (A7) |
| A4 | Wrong version: v2.0 OS is stale against v2.1 | v2.1 has CSD01–CSD04 only (latest 2026-10-21); `/v2.1/os/` = **404**; v2.0's only later stage is Errata 01 (2024-01-26), which changes *only* `aggregator_json_schema.json` | **no** — v2.0 OS is the correct tier-A text; needs a one-line currency disclosure (A4b) |
| A5 | False provenance: "CSAF appears nowhere in the lane" | the before-control's `-> 0` is scoped to 5 paths and excludes captures, where CSAF *does* appear | **not a kill, a defect** if upgraded to a global claim — see corrections |
| A6 | Identity change: S055 was already used as a staged-package pointer and as the r37 "unlisted id" control | r37 control is manifest-scoped and still reproduces (`exit=2`) after S055 lands; r25 pointer line says pointers are "never ids" | **no** — but the number now has three referents in lessons |

## A1 — uncovered ground (the item's first question)

Lane-wide sweep, word-bounded, over exactly the surfaces the item names:

```
cd lane && grep -rniE '\bCSAF\b|\bVEX\b|product_status|advisory format' \
  corpus/knowledge/ corpus/lessons/ considerthese/ corpus/README.md corpus/SOURCES.md \
  corpus/QUALITY.md SKILL.md PROVINCE.md AGENTS.md
```
→ **0 lines**. `corpus/knowledge/*.md` = 50 files, of which exactly one (the new entry) cites
`source: S055`; registry = 55 rows, S055 is the only CSAF row; frontier = 21 rows, F21 the only
advisory-format row.

Restricting to committed captures shows the ground is *approached* but never *mined*:

```
grep -rliE '\bCSAF\b|\bVEX\b' corpus/source-snapshots/
corpus/source-snapshots/round-24/S001.txt
corpus/source-snapshots/round-24/S003.txt
corpus/source-snapshots/round-25/S040.txt
corpus/source-snapshots/round-26/S040-live.txt
```

The four pre-existing mentions are recommendations/availability statements, not semantics:

- `round-24/S003.txt:287` (CISA CVD program, mined under F02): "Publish advisories using the
  Common Security Advisory Framework (CSAF),13" — with footnote 13 pointing at CSAF, no content.
- `round-25/S040.txt:355-356` (Cisco policy, mined under F10): "an option to download Common
  Security Advisory Framework (CSAF) content." / "CSAF is an industry standard designed to depict
  vulnerability information in machine-readable format."
- `round-24/S001.txt:1121-1123` (CVSS v4.0 User Guide, mined under F01) references VEX only to
  borrow the word "affected": "Aligns with “affected” status in [Minimum Requirements for
  Vulnerability Exploitability eXchange (VEX)]()."

Decisive measurement — can any existing capture state F21's substance?

```
for f in round-24/S003.txt round-25/S040.txt round-24/S001.txt:
  grep -cE 'product_status|component_not_present|known_not_affected|VEX-Justification' → 0,0,0
```

So a new source was genuinely required; F21 could not have been mined from an admitted row. The
(row, entry, capture) trio is the right shape. **Attack fails.**

Collision check against the neighbouring rows, since "uncovered" also means "not a duplicate
authority":

- F11 (`iso-29147-and-30111-division-of-labour.md`) mentions advisory only as a *direction*
  ("report receipt and advisory/publication are 29147", :41); no machine-readable format, no JSON,
  no vocabulary. F10 (`vendor-disclosure-policies-as-corpus-objects.md`) has zero hits for
  `machine-readable|CSAF|format`. F18/F19/F20 own prioritization, not product status. No duplicate
  authority.
- Precedent for `kind: spec, tier: A` inside the lane: S002 (CVSS v4.0 spec), S029 (CRA regulation),
  S031 (CNA rules). The row's `spec` kind is not novel.

## A2 — province (the item's second question)

The strongest case against: *CSAF is what a vendor runs on the publishing side; kasegi is
researcher-side, so product_status/justification is publisher engineering that belongs elsewhere.*

Why it fails, on local text:

1. `PROVINCE.md:27-30` — "The line-3 domain comprises program rules, scopes, and claim packages; the
   core also covers triage and claim gates, and **submission/disclosure packaging**." (:30) A machine-readable advisory is disclosure packaging; refusing it would refuse the
   named core.
2. The same reject rule would exclude four already-admitted rows on the same "a researcher never
   writes it" test: F01 (CVSS specification), F07 (CNA operational rules), F08 (CRA statute), F11
   (ISO/IEC division of labour). A rule that reds a quarter of the admitted frontier is over-broad,
   not discriminating.
3. The admitted object is consumer-facing and claim-relevant: `product_status` is where a vendor
   asserts a version is `known_not_affected`, and `/vulnerabilities[]/flags[].label` is the
   machine-readable reason. That is the structured form of "your report is not a vulnerability" —
   a triage/claim fact, not an authoring technique.

It survives only as a **framing constraint**, and the landed entry satisfies it: it is written as a
reader's guide ("How a bounty or security researcher uses it", six steps), carries eight rejected
over-generalizations, and contains no authoring imperative:
`grep -niE 'you (should|must) (publish|author|emit)|to publish a CSAF|authoring' <entry>` → 0 lines.

## A3 / A7 — contested with kake's `CSAF` extension mention

`kake-shokunin/corpus/knowledge/security-txt-publishing.md:63`:
"be ignored (S078); securitytxt.org already lists one extension, `CSAF` (S079)."

That is a *field-cardinality* bullet inside an entry whose scope line reads (kake entry :4): "How a
publisher serves one valid security.txt from GitHub Pages … **Nothing here says what an
operator-owned property serves.**" Its ground is "operability and freshness of the web properties"
(:12). Kake's row for it is `security.txt publishing on GitHub Pages (r35)` (kake README :64) — no
CSAF row, no CSAF source beyond the securitytxt.org field list (kake S079). Kake states that a
field exists; kasegi states what a VEX document's statuses and justification labels mean. No
shared load-bearing claim, so **not contested**.

The mention does install a fence that a later round can walk through: the *discovery/serving*
surface (`/.well-known/csaf/`, `provider-metadata.json`, the `CSAF` field pointing at it) is kake's
ground under PROVINCE "Sibling lanes are reported, not absorbed". Measured on the landed entry:

```
grep -niE 'well-known|provider.?metadata|security\.txt|aggregator|rolie|feed' <entry>
17:- … "This prose specification is one component of a Work Product that also includes:" (L27)
    — the aggregator, CSAF and provider JSON schemas (L28-L33), which are not in this capture.
```
One hit, and it is the required work-product disclosure, not serving guidance. **Complies.** Keep
it that way; an r39 deepening of this row must not drift into provider metadata.

## A4 — v2.0 OS versus v2.1 (the item's version question)

Measured against the OASIS file tree (all fetches `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`):

```
GET /csaf/csaf/                      → 200,   392 B : v2.0/ (12-Feb-2024), v2.1/ (21-Oct-2026)
GET /csaf/csaf/v2.0/os/              → 200,   929 B : csaf-v2.0-os.{html,md,pdf,zip}, manifest, schemas/
GET /csaf/csaf/v2.0/errata01/        → 200,   817 B : csaf-v2.0-errata01.{html,md,pdf}, csd01/, os/
GET /csaf/csaf/v2.1/                 → 200, 1,097 B : csd01/ csd02/ csd03/ csd04/ schema/ + csaf-v2.1.{html,md,pdf}
GET /csaf/csaf/v2.1/os/csaf-v2.1-os.html → 404, 41,334 B ("Not found")
```

So there is **no** CSAF 2.1 Committee Specification and no 2.1 OASIS Standard: the v2.1 line has
stopped at CSD04 (directory `csd04/`, document dated 21-Oct-2026; HTML 1,231,332 B and Markdown
855,161 B, both HTTP 200).
v2.0's only stage after `os` is **Errata 01, OASIS Approved Errata, 26 January 2024**, and the
errata text settles the question itself:

> "There are no changes to the published CSAF document. Changes have been made only to the
> included Aggregator JSON schema." … "The only approved change is to the Aggregator JSON schema
> file … In line 178 of the aggregator_json_schema.json, the entry `mirror` as required field has
> been corrected to be `mirrors`" … "The conformance requirements stated in the OASIS Standard
> Common Security Advisory Framework Version 2.0 [csaf-v2.0-os] are not changed in any way."

Corroborated structurally: the v2.0 CSAF JSON schema at the OS path and at the top level are the
same bytes — `sha256 29c114b35b0a30831f1674f2ab8b3ed9b2890cfeaa63b924ac6ed9d70ef44262` for both
`/v2.0/os/schemas/csaf_json_schema.json` and `/v2.0/csaf_json_schema.json` — and contain exactly
the vocabulary F21 claims:

```
flag label enum: component_not_present, inline_mitigations_already_exist,
  vulnerable_code_cannot_be_controlled_by_adversary, vulnerable_code_not_in_execute_path,
  vulnerable_code_not_present
product_status keys: first_affected, first_fixed, fixed, known_affected, known_not_affected,
  last_affected, recommended, under_investigation
```

CSAF 2.1 CSD04 still carries the same five codes (same per-token counts as v2.0) and still has
`Profile 5: VEX`, so the vocabulary is not in flight either. **v2.0 OS is the right tier-A source;
v2.1 would have been the wrong citation (a draft with no CS/OS stage).**

**A4b — the precision defect.** The OS's own title block marks the *authoritative* component as the
`.md` (`https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.md (Authoritative)`, capture L5),
and the v2.0 line's own "Latest stage" pointer (`/v2.0/csaf-v2.0.html`) resolves to **Errata 01**,
not to `/v2.0/os/`. The landed entry's "Honest limit" says "One stage pinned … a later stage is a
new pin, not a correction" and does not name either fact. An outside verifier looking for currency
will find both in five minutes and read the silence as unawareness. This is the one substantive
gap I found in the admission as recorded.

## A5 — the sweep's `0` is scope-local (false-provenance risk)

`c2-controls/before.txt` records:

```
uncovered-ground sweep: grep -rliE 'CSAF|Common Security Advisory Framework|\bVEX\b' \
  corpus/knowledge corpus/README.md corpus/SOURCES.md SKILL.md PROVINCE.md | wc -l -> 0
```

That command is honest — it names its five paths, and `corpus/source-snapshots/` is not among
them. But the same file's neighbouring sibling sweep already had to correct a similar
over-generalisation ("1 file: kake-shokunin/…/security-txt-publishing.md:63 … adjacent … not
CSAF/VEX ground"). The risk is inheritance: a lesson or report sentence of the form "CSAF appears
nowhere in the lane / the sweep found zero" is **false** against local evidence — 4 committed
captures carry the string, and `round-24/S003.txt:287` is a *mined* row (F02). The defensible
sentence is the vocabulary-level one, which A1 measures: no entry derives a CSAF fact, and no
pre-existing capture contains `product_status`/`known_not_affected`/`component_not_present`.

## A6 — S055 identity

- `corpus/lessons/round-25.md:107` — `| S036 (S055) | 脆弱性情報ハンドリングポリシー (Cybozu) | …`, in a
  table whose preamble says "the staged-package ids in parentheses are pointers, **never ids**".
- `corpus/lessons/round-37.md:115` — "`--source S055` gives `UNAVAILABLE reason=not-listed exit=2`"
  as the unlisted-id negative control.

Re-ran the r37 control today, before and after the C2 landing:

```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S055
S055:source UNAVAILABLE reason=not-listed
exit=2
```

It still reds because the "not-listed" branch filters **the manifest's records** (`source-recheck.py:225-229`),
not the SOURCES registry, and round-37's manifest holds S054 only. The historical assertion is
therefore not falsified by the admission. Registry arithmetic is also clean: ids S001–S054 are
contiguous with no gaps, S030 is superseded (not retired) by S031, so S055 is the append-only next
id per the registry contract, and no `S055.txt` exists in any other round dir
(`ls corpus/source-snapshots/*/S055.txt` → all "No such file"). Non-issue, worth one line of
disclosure in the r38 lesson only because a reader grepping `S055` across `corpus/lessons/` now
finds three referents.

## Capture and instrument sanity (independent, not the C2 reviewers' work)

```
sha256sum corpus/source-snapshots/round-38/S055.txt
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42   (5,146 lines, 272,441 B)
manifest: sha256 63c8ad52…, raw_sha256 fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b

my own GET of the same URL, 18:36:32Z and again 18:40:33Z:
  http=200 bytes=414858, sha256 fad0c60d… (identical to both the manifest's raw_sha256 and each other)
  last-modified: Sun, 05 Apr 2026 13:17:09 GMT; cache-control: public, max-age=31536000, immutable

python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=2135-ok
S055:Q2 OK occurrences=1 anchor=2844-ok
S055:Q3 OK normalized=markup-whitespace occurrences=1 anchor=2151-ok
S055:Q4 OK occurrences=1 anchor=1767-ok
exit=0
```

The capture is byte-reproducible from the live URL, every quote binds exactly once, and Q3's
declared `normalized=markup-whitespace` is honest — the profile sentence really is split across
capture L2151/L2152 (`For each item in` ends L2151), which I verified by reading L2130-L2160.

One further check that the *ground* is real, not an artifact of the manifest's four quotes:
`grep -c 'impact_statement' S055.txt` → 0; the v2.0 machine-readable not-affected form is
`/vulnerabilities[]/flags[].label`, and §6.1.27.9 requires "a corresponding impact statement exist
in /vulnerabilities[]/flags or /vulnerabilities[]/threats" for every `known_not_affected` product.
F21's wording ("machine-readable not-affected justification flags") is accurate for v2.0 and would
have been wrong for a CSAF 1.2/VEX `justification` field — worth preserving if the row is ever
re-worded.

## Impacted axes

- `coverage` (C2, held 7): **no change.** A1/A2/A3/A4/A6 all fail as kills; the row, entry and
  capture are the right shape and the source is the right tier and version. The admission is
  defensible against the item's four questions: yes uncovered (vocabulary-level), yes in province
  (disclosure packaging, consumer-side), no not contested by kake's field mention, and v2.0 OS is
  correct against a v2.1 that has no CS/OS stage.
- `coverage` — residual risk if the record over-claims (A5): one false global sentence ("CSAF
  appears nowhere in the lane") would be falsified by `round-24/S003.txt:287`, a *mined* row's
  capture. That is a provenance defect, not a coverage one, but it is the kind of sentence a
  verifier greps for.
- Other axes: untouched. Nothing here asks for a re-scope, a new source, or a changed count.

## Smallest safe corrections

Ordered, smallest first. None is a blocker; #1 is the only one I would insist on.

1. **Cap the sweep sentence (A5).** Anywhere round 38 records the uncovered-ground measurement,
   keep it path-scoped or state it at vocabulary level. Defensible form: "no knowledge entry,
   registry row, README, SKILL or PROVINCE line names CSAF; four committed captures (S001 r24,
   S003 r24, S040 r25, S040-live r26) mention it only as a recommendation or an availability note,
   and none carries `product_status` / `known_not_affected` / `component_not_present`."
2. **Disclose the version line (A4b).** One sentence in the entry's Honest limit, owned by the C2
   entry seat, not by this seat: "The authoritative component is `csaf-v2.0-os.md`; this capture is
   the published HTML rendering. Later stages were checked on 2026-10-26: Errata 01 (OASIS Approved
   Errata, 26 Jan 2024) changes only `aggregator_json_schema.json` (`mirror`→`mirrors`) and states
   'There are no changes to the published CSAF document'; CSAF 2.1 has reached CSD04 (21 Oct 2026)
   with no CS or OS stage (`/csaf/csaf/v2.1/os/` = 404)." This also hands the next verifier the
   check instead of a silence.
3. **Keep the kake fence explicit (A3/A7).** If the entry is ever extended, the extension belongs
   to document vocabulary, not to discovery/serving (`/.well-known/csaf/`, `provider-metadata.json`,
   the security.txt `CSAF` field) — that surface is kake's under PROVINCE "reported, not absorbed".
   The landed entry already complies; no edit needed now.
4. **One-line id note (A6).** Optional: "S055 was a round-25 staged-package pointer (never a lane
   id) and the round-37 unlisted-id control number; the registry's next append-only id is S055."
   Costs a line, prevents a false-provenance reading of `corpus/lessons/round-25.md:107`.
5. **Do not re-word the flags as `justification` fields.** If F21's topic line is ever edited, keep
   "machine-readable not-affected justification flags" (true for `flags[].label`) and never
   "product_status.justification" (no such element in v2.0; `impact_statement` appears 0 times in
   both the OS prose and the OS schema).

## Fetch log (UTC, instrument UA `kasegi-shokunin/1.0`, `--max-time 90`)

| time | URL | status | bytes |
|---|---|---|---|
| 18:36:32Z | `…/csaf/csaf/v2.0/os/csaf-v2.0-os.html` | 200 | 414,858 |
| 18:36:32Z | `…/csaf/csaf/v2.1/os/csaf-v2.1-os.html` | 404 | 41,334 |
| 18:36:33Z | `…/csaf/csaf/v2.1/csaf-v2.1.html` | 200 | 1,231,332 |
| 18:36:34Z | `…/csaf/csaf/v2.1/` (index) | 200 | 1,097 |
| 18:36:34Z | `…/csaf/csaf/` (index) | 200 | 392 |
| (batch, after 18:36:34Z) | `…/csaf/csaf/v2.0/` and `…/v2.0/os/` (indices) | 200 | 1,704 / 929 |
| 18:37:22Z | `…/csaf/csaf/v2.0/errata01/` (index) | 200 | 817 |
| 18:37:57Z | `…/csaf/csaf/v2.0/errata01/os/` (index) | 200 | 1,001 |
| (batch, after 18:37:57Z) | `…/v2.0/errata01/csaf-v2.0-errata01.html` | 200 | 25,631 |
| (batch, after 18:37:57Z) | `…/v2.0/csaf_json_schema.json` | 200 | 57,152 |
| 18:38:52Z | `…/v2.1/csd04/csaf-v2.1-csd04.html` | 200 | 1,231,332 |
| 18:38:53Z | `…/v2.1/csd04/csaf-v2.1-csd04.md` | 200 | 855,161 |
| (batch, after 18:38:53Z) | `…/v2.0/os/schemas/csaf_json_schema.json` | 200 | 57,152 |
| 18:39:16Z | `…/v2.0/csaf-v2.0.html` (v2.0 "latest stage") | 200 | 25,631 |
| 18:40:33Z | `…/v2.0/os/csaf-v2.0-os.html` (reproducibility refetch) | 200 | 414,858 |

Fetches without their own timestamp line were issued in the same instrument batch as the stamped
one immediately above them; the v2.0 OS document's `Date`/`Last-Modified` headers are recorded in
the capture-sanity block. No credential, session, private URL or operator-owned host was contacted,
and no live target was touched.

## Scratch and tooling

Scratch `S=/fast/scratch/hyaku/kasegi-r38/CritC2Ground/` (created with `mkdir -p`, `TMPDIR`-independent,
pages fetched into `$S`) was removed before yield per the seat contract. No tool was installed or
upgraded this seat; the working tools were the pre-existing `curl`, `python3`, `git` (read-only),
`grep`, `sha256sum`. No `pacman`, no network write, no mutating git/jj command, no writes outside
this receipt.
