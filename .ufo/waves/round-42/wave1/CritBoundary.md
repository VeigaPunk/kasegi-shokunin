# CritBoundary — F25 candidate shared-ground boundary check (receipt-only)

run-utc: 2026-10-28T11:08Z · seat: CritBoundary · scope: boundary check only — per-candidate
disjointness verdicts for the F25 pick; no deliverable text files; no lane writes outside
this receipt. Scratch `S=/fast/scratch/hyaku/kasegi-r42/CritBoundary` removed before yield.

Verdict summary: **BOTH candidates DISJOINT — admit-either, with one wording guard each.**
Neither candidate has a held lane row/entry covering its document family, no sibling lane
holds either doc family, and the held-row boundaries are structural (rules vs schema;
VEX/status vocabulary vs affected-set algebra), not merely organizational.

## 1. CVE Record Format 5.x vs held rows S030/S031 — DISJOINT, guard G1 required

Held ground read (all committed bytes):

- `corpus/SOURCES.md:36-37` — S030 = CNA Operational Rules **v4.2.0**, S031 = **v4.2.6**;
  both row scopes read "CVE Program CNA scope, vulnerability determination and
  assignment requirements". Knowledge entry `corpus/knowledge/cna-assignment-and-
  vulnerability-rules.md` covers only rules 3.1, 3.2.4.2, 4.1, 4.2 (its pinned quote
  table ends at 4.2.12; frontier topic F07 admits it as "CVE CNA operational rules").
- **Strongest counterexample tested:** S031's own capture `corpus/source-snapshots/
  round-23/S031.txt:108` contains `5 CVE Record Content This section specifies what
  information is in a CVE Record` with rules 5.1.1–5.4.2 (required record content,
  public references, example IDs). If "record content" were indivisible, the format
  doc would already be covered.
- Why disjointness still holds — the doc itself draws the line:
  - S031.txt §5.1.12: `MUST meet any requirements set by any approved formats or
    submission mechanisms, for example, the CVE Record Format and the Record
    Submission and Upload Service (RSUS)` — the rules *defer outward* to the format
    as a separate normative artifact.
  - §5.1.13: `MAY contain optional elements supported by the CVE Record Format` —
    format-superset acknowledgement, not schema text.
  - §5.2: `Through automation efforts such as the CVE Record Format and CVE
    Services, the content of the prose description … is becoming less important` —
    the rules name the format as machinery, and only constrain prose-level duties.
  - No lane row or entry covers the bundled JSON schema or `schema.cve.org` docs;
    `grep -rniE 'cve.?record.?format|cve-schema|schema\.cve'` over corpus/ finds
    only the S030/S031 *rule references* above plus `cisa-cvd-program-stages.md`
    ("CVE Record Determination" = a workflow stage about whether a record exists,
    not its structure).
- Verdict: rules govern *who must write what*; the schema governs *field structure/
  types* — disjoint, same family split the lane already applies (F07 rules beside
  F21/F23 schemas). S031 §5 is a mirror of required content, not a schema.

**G1 (smallest safe correction if picked):** the F25 entry must pin quotes to the
schema artifact (field/type/object vocabulary) and NOT re-derive S031 §5.1–5.4
content obligations as a "new" claim; cite S031 §5.1.12 as the delegation rule.
Re-claiming §5 as fresh ground would make the scout's no-overlap check effectively
false at the capture level (kill rule: "the chosen topic's document already
covered by a lane row or entry").

## 2. OSV schema vs held advisory-doc rows S055/S060 (+ S056/S058/S061/S062) —
DISJOINT, guard G2 required

Held advisory/exploitability family inventory (SOURCES.md rows read directly):

- S055 CSAF 2.0 VEX profile (F21) — 8 `product_status` lists, 5 not-affected
  justifications; publisher product-status *assertion* vocabulary.
- S060 CycloneDX v1.7 `vulnerabilities[].analysis` (F23) — 6 analysis states, 9
  justifications, 5 responses; *analyst-decision* object inside a BOM.
- S056 CISA Minimum VEX Requirements; S058 OpenVEX spec v0.2.0 (4 status labels +
  5 justifications); S061 CISA VEX Status Justifications PDF (label origin doc);
  S062 CSAF v2.1 csd04 (flip monitor, status B — still CSD, no `os/` per its own
  captured listing).
- Distinct schema surface test (the thing OSV has that none of the above does):
  OSV's claim is the `affected[]` record algebra — `ranges[].type` (GIT/SEMVER/
  ECOSYSTEM) × `ranges[].events[]` (introduced/fixed/last_affected/limit) ×
  `versions[]` enumeration. That is version-interval *set* construction. CSAF/
  OpenVEX bind product→status *labels*; CycloneDX `analysis` records a decision
  *about* a vuln already in a BOM. Nearest shared construct: CycloneDX
  `affects[].versions[].range` (S059/S060 slice L69–L103) — but per S060.txt the
  `vers:` range *syntax* is imported from an external spec, not defined in-page.
- kaidoku sibling OSV use: `kaidoku-shokunin/corpus/SOURCES.md:21` S015 =
  `api.osv.dev/v1/vulns/CVE-2025-55305` (type `dataset`, knowledge target
  `corpus/lessons/round-13.md`) — one **record instance** consumed as an RE
  precondition. Already adjudicated in this lane's committed
  `.ufo/waves/round-23/falsify/SiblingOverlap.md` §2.2: "an OSV record consumed
  as a reverse-engineering *precondition* for an Electron fuse. It states no
  CNA assignment rule, no assigner scope, and no reporting duty." Schema doc ≠
  schema instance — no substantive sibling ground.
- Verdict: OSV is a distinct schema surface — the advisory family never defines
  affected-interval algebra.

**G2 (smallest safe correction if picked):** the entry must (a) attribute `vers:`
ranges to the vers spec, not claim range syntax as OSV's own; (b) not re-derive
VEX status/justification claims (S056/S058/S061 cover that label space — an OSV
`database_specific` echo of those labels is out of F25's row); (c) in the S0NN
registry note, flag the kaidoku S015 namespace (S015 = CWE Top 25 here, OSV
record there — IDs are not fleet-unique joins, per the r23 finding).

## 3. kake / kengaku corpora — clean for both candidates

- `grep -rniwE 'osv|osv\.dev'` + `grep -rniE 'cve.?record.?format|cve-schema|schema\.cve'`
  over `kake-shokunin/corpus/` and `kengaku-shokunin/corpus/` (SOURCES.md +
  knowledge/ + SKILL.md): **0 doc-family hits** (kake hit is `osv`-substring in
  binary pack noise only; kengaku hits are `osv-scanner` binary listings in r41
  falsify receipts — a tool binary, not a doc).
- Fleet-wide sweep (all 19 siblings): `osv-schema|ossf\.github|CVE_Record_Format|
  cve-schema|schema\.cve\.org|cveawg` → 0 hits in every lane's corpus/SKILL.md.
- Precedent that fired the park: kake `corpus/knowledge/security-txt-publishing.md`
  cites S078 RFC 9116 + S082 RFC 8615 — sibling-held ground under the F24 topic;
  that is the overlap class that must not recur. Neither OSV-schema nor
  CVE-Record-Format families appear in kake (domain: web properties/publishing)
  or kengaku (domain: LLM eval).

## 4. Evidence — commands and observed output

```
$ mkdir -p $S && bash .../disk-guard.sh status        -> green (27% used on /fast/scratch/hyaku)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   -> 63
$ ls corpus/knowledge/*.md | wc -l                                    -> 60
$ grep -nE '^\|[[:space:]]*S(030|031|055|060)\|' corpus/SOURCES.md      -> rows as quoted above (lines 36,37,61,66)
$ grep -nE '^\|[[:space:]]*S0(56|58|59|61|62|63)\|' corpus/SOURCES.md   -> S056-S063 rows as quoted (lines 63-69)
$ grep -oE '^\| S[0-9]+ \| [^|—]+' corpus/SOURCES.md                    -> full title list; no OSV-schema / CVE-Record-Format row
$ sed -n '100,135p' corpus/source-snapshots/round-23/S031.txt           -> §5 text incl. 5.1.12/5.1.13/5.2 delegation quotes above
$ head -60 corpus/knowledge/cna-assignment-and-vulnerability-rules.md   -> quote table ends 4.2.12; no §5 schema claims
$ head -50 corpus/knowledge/csaf-vex-product-status-and-justifications.md -> VEX status-label ground (L2844, L2151-52)
$ head -50 corpus/knowledge/cyclonedx-analysis-subtree.md               -> analysis-subtree ground; vers imported (L69-L103 slice)
$ grep -rniwE 'osv' /home/vgpnk/Projects/shokunin/*-shokunin/...        -> kaidoku S015 only + binary/tool-name noise
$ for lane in *-shokunin; do grep doc-family ...; done                  -> 0/19 siblings
$ grep -nE 'F24' corpus/README.md ; sed -n '545,565p'                   -> F24 row status=admitted, S063, entry rfc-9116-security-txt.md
```

## 5. Impacted axes

- coverage: both picks keep C2's no-overlap kill clause green *if* the guard
  sentence (G1 or G2) lands in the entry/amendment text; OSV is the marginally
  safer pick (widest structural distance from S055/S056/S058/S060/S061/S062
  label-space and from S031 §5 prose).
- depth:verifiability: unaffected — receipt-only.

Not a kill-rule defect; a tradeoff the scout gates must arbitrate. Disagreement
surfaced for the canonical judge: the CVE-Record-Format pick carries the S031-§5
mirror risk (content vs structure) that a strict sibling-overlap auditor could
score against; OSV carries the weaker vers-attribution risk only.
