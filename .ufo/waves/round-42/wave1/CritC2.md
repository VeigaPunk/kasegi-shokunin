# CritC2 — attack on frozen C2 (round 42, wave 1)

Seat: CritC2 (critic, receipt-only). Scope: the three assigned attacks on the frozen
coverage claim C2 in `.ufo/waves/round-42/claims.json`. All commands run at base
`5053a7f46de35784cff4b56756906e9014a38276` (pre-F25 state; lane working tree unchanged
— no lane files written by this seat).

Axes in play: `coverage` (does F25 add real, non-duplicate, in-province ground) and
`depth:verifiability` (is the claim's evidence chain machine-checkable at the promised
level).

---

## Attack 1 — is the OSV / CVE-Record lead class in-province and distinct from held ground?

**In-province: DEFENDED.** The lane's frontier already admits exactly this class —
machine-readable vulnerability-data standards — six rounds running:

- F18 CISA KEV catalog (S052 JSON feed), F19 FIRST EPSS (S053), F20 SSVC (S054),
  F21 OASIS CSAF v2.0 VEX (S055), F22 CISA When-to-Issue VEX (S057), F23 CycloneDX
  v1.7 `vulnerabilities[].analysis` (S060), F24 RFC 9116 (S063) — all read from
  `PROVINCE.md` frontier amendments and `corpus/README.md` frontier rows.
- OSV schema (the OSV advisory record format) and the CVE Record Format (the canonical
  CVE record schema) are the same family: machine-readable vulnerability-data
  interchange formats of direct use in bounty/security research. Fit is not the
  question.

**Distinctness in-lane: DEFENDED with one ambiguity to name.**

Observed (base, live greps):
- `grep -rn 'OSV' corpus/ SKILL.md` → 0 hits (the boundary-regex run over
  `corpus/ SKILL.md` printed nothing for `\bOSV\b`, `ossf.github.io`,
  `open.source.vulnerab`; earlier broad hits like S012's "open-source vulnerabilities"
  are English text, not the schema).
- `grep -rniE 'cve-schema|CVE_Record_Format|schema\.cve\.org|cve record format' corpus/ SKILL.md`
  → 4 hits, all inside `corpus/source-snapshots/round-23/S031.txt` (the CNA Rules
  capture): 4.5.3.5-4.5.3.7 "CVE Record(s)", 5.1.12 "MUST meet any requirements set by
  any approved formats or submission mechanisms, for example, the CVE Record Format",
  5.2 "Through automation efforts such as the CVE Record Format and CVE Services…".
- `corpus/SOURCES.md` rows: 63 rows, max id S063, 10 already `status=rejected`.
  No OSV row; S030/S031 cover CNA *rules*, not the Record Format schema.
- `corpus/instruments/knowledge-expected.txt` (60 entries): no OSV/CVE-Record entry.
- `kaidoku-shokunin/corpus/SOURCES.md:21` S015 — mined row "OSV CVE-2025-55305
  record — https://api.osv.dev/v1/vulns/CVE-2025-55305 | dataset | A | The OSV
  record's affected-version, fix-reference, and fuse-precondition fields" — a sibling
  lane holds a mined OSV **record instance** row (dataset tier A). `kotodama-shokunin`
  hit is a linguistics false positive ("OSV" = Object-Subject-Verb word order).
- `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` (96 staged rows):
  no `OSV`/`cve-schema`/`CVE_Record`/`schema.cve` match — no assimilation collision
  for either candidate.

Reading: no lane row or entry covers either *document*. The ambiguity is what counts
as coverage for the scout's no-overlap check:

- The spec (`wave1-spec.json` ScoutF25Lead) bounds the check to `corpus/SOURCES.md +
  corpus/knowledge/*.md + corpus/README.md` — the **captures** (`source-snapshots/**`)
  are not in the enumerated surface, and the lane's own S031 capture already talks
  about the CVE Record Format four times. A "mention is not coverage" ruling keeps
  CVE Record Format eligible; a stricter verifier could read S031's capture as held
  ground. The freeze does not pin which.
- **Sibling overlap is the sharper problem.** The frozen kill rule says only "the
  chosen topic's document already covered by a **lane** row or entry". The r41 F24
  failure mode (kake's `security-txt-publishing.md` overlap found post-admission,
  parking F24 pending an L0 ruling) is *not* frozen into the kill rule — the seat
  spec mandates the sibling check, but the claim does not. Kaidoku S015 is a mined,
  tier-A sibling row in the same document family as OSV (a record instance built on
  the OSV schema; its fields `affected`, `ranges`, `references` are the schema's
  subjects). By F24 precedent that is substantive sibling ground: an OSV-schema pick
  admitted over kaidoku S015 repeats the exact round-41 failure pattern, and the
  frozen kill rule as worded does not fire on it.

Verdict: the lead class is in-province and both named candidates are in-lane distinct;
**the CVE Record Format is the safer pick** (no sibling ground found anywhere on the
fleet; the four hits are capture text the no-overlap surface does not enumerate). The
OSV pick passes the frozen letter but carries a live sibling-overlap exposure — the
freeze should have named sibling ground in the kill rule. **DEFENDED for the class;
ROUTED defect: sibling-overlap not kill-bound.**

## Attack 2 — can a do-nothing scout pass the screen?

**DEFENDED on the admit side; the screen's discernment is only text-verified.**

A scout that does nothing cannot fabricate the admit: `S064.txt` capture bytes are
bound by `manifest.json` sha256 → `source-recheck.py` → `capture-binding-check.py` →
`recheck-audit.py` → `frontier-recheck-count.py` PASS F25 → `knowledge-expected.txt`
(→61) → census exit 0. `c2-controls/before.txt` shows all after-values unreachable at
base (frontier 24, registry 63, harness entries=27, binding 55, audit expected=60).
The pick's two named candidates are both live and distinct — observed this round:

- `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://ossf.github.io/osv-schema/`
  → HTTP 200, 228,890 bytes, sha256 `8cf1e3d3f9e10eba902d03af6c281d6bc5e71c22dc351fcb4b811c64030570e8` (fetched 2026-10-28T11:11:42Z)
- `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://raw.githubusercontent.com/CVEProject/cve-schema/main/schema/docs/CVE_Record_Format_bundled.json`
  → HTTP 200, 133,616 bytes, sha256 `44c703322b1fcc532bc1c93f3993a0ba042c1a2831aae8cf39c4fbb707d03c8f` (fetched 2026-10-28T11:11:42Z)

So the *admission* cannot be do-nothing. What a do-nothing screen *can* pass: the
no-overlap check itself (a scout that greps only the three enumerated surfaces —
which exclude `source-snapshots/**` and every sibling lane — satisfies the spec
letter while performing a weaker check than the F24 failure demands), and the
**reject record** — see attack 3. The claim's outcome is protected by the kill
rule's "no-overlap check false" clause, but the check's *execution* is asserted, not
bound to evidence.

## Attack 3 — does the ≥1-reject requirement invite a fabricated rejection?

**FIRES (evidence asymmetry) — and the frozen registry counter contradicts the
registry-row form of the reject.**

1. **Binding asymmetry.** Every admit artifact is machine-bound (capture sha256 in
   manifest, instrument re-check, binding, audit). The reject artifact is a Gate-block
   line: URL + date + ≤25-word located quote + reason + flip. Nothing committed
   carries the rejected document's bytes, so the quote is unverifiable without a live
   re-fetch — strictly weaker than the admit's quote, which is verifiable offline
   against the committed capture. A reject fabricated against a real URL with a
   plausible invented quote passes every frozen counting command and the kill rule's
   presence check ("no screened reject recorded in the Gate block"). `QUALITY.md`
   carries no criterion binding rejected-candidate evidence (Q3/Q5 cover *entry*
   quotes and rejected *over-generalizations*, not screened-source rejections).
   Precedent already holds the stronger form the freeze declined to require: rejected
   rows S056/S058/S059 anchor to `ScoutVexLeads.md`/`ScoutS060Leads.txt` fetch ledgers
   with fetch UTC + bytes + sha256 (SOURCES.md:63-65). Requiring the Gate reject to
   name `fetched <UTC>, <bytes>, sha256 <hex>` or `unfetched, reason <x>` would make a
   fabricated reject falsifiable in one command — the same binding the admit side
   already gets free.

2. **Counting contradiction.** Frozen counting command 2:
   `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 63 -> 64`.
   Observed at base: prints `63` (10 of the 63 are `status=rejected` rows — S022,
   S024, S026–S028, S056, S058, S059, S061, S062 — all in the `## Registry` table, all
   matching the regex). The claim and milestone demand "at least ONE rejected
   screened row S065+" and the wave spec orders ExecC2Rows to build "S065 rejected
   row(s) … status rejected, reason+flip, used-by `—`"; CritSync's own attack list
   asks whether a rejected S065 row counts as registry growth. A row-shaped
   `| S065 | … | rejected | … |` appended in Registry (the only shape consistent
   with the S059 precedent and census rule E12, which flags row-shaped sources
   outside `## Registry` as E12) makes the command print `65`, not the frozen `64`.
   Either the expected value `63 -> 64` is wrong (should be `64+R` / `>=64`, matching
   the milestone's "registry 63 -> 64+R (R>=1)"), or the "rejected row" must land as
   lead-level prose (consistent with D-r41-2's "a lead-level rejection suffices",
   `round-41-verifier-spotcheck.md` §5.2) — but then the S065+ *naming* and the
   seat spec's "rejected row(s)" promise are the wrong shape. As frozen, the two
   statements disagree; the verifier will read it against the strictest limb.

3. **Structural triviality of the reject.** Candidates ≥ 2, pick = 1: a reject is
   guaranteed to exist, so D-r41-2 is closable by construction with any reason.
   Acceptable *iff* the reason+flip is honest — which is exactly the unbound limb in
   (1).

## Smallest safe corrections (routed, in-priority order)

- **R-C2a (verifiability, reject evidence):** Gate reject record must carry the
  rejected doc's fetch receipt — `fetched <UTC>, HTTP <code>, <bytes> B, sha256 <hex>`
  — or an explicit `unfetched` marker with the reason the fetch was not needed; the
  rejected registry row's anchor cell names `ScoutF25Lead.reject-record.txt` / fetch
  ledger (S056/S058/S059 precedent). Kills fabricated-quote rejects in one re-check.
- **R-C2b (satisfiability, registry counter):** disambiguate the reject's landing —
  either expect `64+R` in counting command 2 for in-registry rejected rows, or name
  the reject a lead-level prose record outside the Registry table (and drop the
  "S065+ row" phrasing). Spec/freeze disagree today.
- **R-C2c (distinctness, sibling ground):** add sibling ground to the C2 kill rule
  ("…or a sibling lane row/entry") or bind the scout's sibling verdict as committed
  evidence the verifier can weigh; OSV is exposed via kaidoku S015 (mined OSV record
  row). The CVE Record Format pick has no observed sibling ground.
- **R-C2d (coverage oracle):** pin the no-overlap surface — do capture-text mentions
  (S031.txt's four CVE-Record-Format mentions) count as coverage? Rule explicitly:
  document-level (row/entry) vs mention-level (capture contents).

## Evidence ledger

| fact | command / source | observed |
|---|---|---|
| registry rows at base | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `63` |
| rejected rows counted | `grep -cE '^\|[[:space:]]*S[0-9]+.*\|[[:space:]]*rejected[[:space:]]*\|' corpus/SOURCES.md` | `10` (S022, S024, S026–S028, S056, S058, S059, S061, S062) |
| max S-id | `grep -oE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md \| sort` | `S063` |
| lane OSV ground | `grep -rn 'OSV' corpus/ SKILL.md` | 0 hits |
| lane CVE-Record ground | `grep -rniE 'cve-schema|CVE_Record_Format|schema\.cve\.org|cve record format' corpus/ SKILL.md` | 4 hits, all in `source-snapshots/round-23/S031.txt` |
| sibling OSV | grep over all `*-shokunin` corpus/knowledge+SOURCES+SKILL | `kaidoku` S015 (mined, tier A, OSV record); `kotodama` linguistic false positive |
| shokuknow collision | `grep -nE 'OSV|cve-schema|CVE_Record|schema\.cve' merge/kasegi/{SOURCES.append.md,MERGE-REPORT.md}` | 0 hits (96 staged rows) |
| OSV doc fetch | `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://ossf.github.io/osv-schema/` | HTTP 200, 228,890 B, sha256 8cf1e3d3…570e8, 2026-10-28T11:11:42Z |
| CVE Format fetch | `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://raw.githubusercontent.com/CVEProject/cve-schema/main/schema/docs/CVE_Record_Format_bundled.json` | HTTP 200, 133,616 B, sha256 44c70332…3c8f, 2026-10-28T11:11:42Z |
| reject-evidence precedent | `corpus/SOURCES.md` S056/S058/S059 anchor cells | fetch ledger with UTC+bytes+sha256 |
| instrument binding | `corpus/instruments/{source-recheck,capture-binding-check,frontier-recheck-count,recheck-audit}.py` headers | admit side bound; no rejected-row binding path |
| census rules | `scripts/sources-census.sh` header | E07 status enum {queued,mined,rejected}; E12 row outside Registry; W02 rejected thin teaches |
| D-r41-2 text | `corpus/lessons/round-41-verifier-spotcheck.md` §5.2 | "screen ≥1 candidate and record a reject with reason + flip (a lead-level rejection suffices)" |

## Verdicts

| attack | verdict |
|---|---|
| 1 — lead class in-province / distinct | DEFENDED (class in-province; both candidates in-lane distinct). ROUTED: sibling ground absent from kill rule (kaidoku S015 vs OSV); no-overlap surface ambiguity (S031 capture mentions). |
| 2 — do-nothing scout passes | DEFENDED on admission (all after-values machine-bound, unreachable at base); the screen's *process* (no-overlap execution, sibling check) is asserted not bound — ROUTED. |
| 3 — ≥1-reject invites fabrication | FIRES: reject evidence is text-only, strictly weaker than admit binding and weaker than the lane's own rejected-row precedent (no fetch receipt mandated); plus the `63 -> 64` counting command contradicts an in-registry S065 rejected row — a satisfiability defect. Smallest corrections R-C2a..d above. |
