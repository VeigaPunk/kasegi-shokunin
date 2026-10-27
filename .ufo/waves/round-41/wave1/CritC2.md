# CritC2 — attack on frozen C2 (F24 / RFC 9116 security.txt)

Seat: critic, receipt-only. Base `5b29ea14`, freeze `fbba3d96`. All work in scratch
`/fast/scratch/hyaku/kasegi-r41/CritC2/` (removed at yield). No lane/fleet writes beyond
this receipt. Tooling: none installed (pacman paused; curl/python3/git already present).

## A1 — Is RFC 9116 in-province? (bounty/security research — disclosure-channel discovery)

**For in-province.** PROVINCE.md Core covers "submission/disclosure packaging" and the
Frontier is "general practice that governs every program". security.txt is the researcher-side
discovery mechanism for the disclosure channel itself — its abstract says it exists "to help
organizations describe their vulnerability disclosure practices to make it easier for
researchers to report vulnerabilities" (fetched text L13-17). Kasegi's own SKILL.md already
operates the rule the spec governs: row "RFC 9116 security.txt — A stub is not a scope …
No assets + no grant → park" (SKILL.md:131), and `vdp-disclosure-packages.md:13` records a
live disclosure routed via "the vendor's security.txt `Contact:` → HackerOne
embedded_submissions URL". F10 ("vendor-side disclosure policies as corpus objects", S036-S040)
is the same surface from the document side; F24 is the machine-readable pointer to that
document — the claim's own ExecC2Rows spec says the entry "complements F10 policy intake
channels". New ground exists: the corpus holds no first-party text for the field grammar,
Expires staleness semantics, or the Encryption pointer rule — the SKILL table asserts
"stub ≠ scope" operationally without grounding it in §2.5.3/§2.5.5.

**Against (strongest counter).** Sibling `kake` (web properties) holds RFC 9116 as S078
(spec, tier A, mined 2026-10-22) with entry `security-txt-publishing.md` — a claimed
admission of the same source document, so F24 could read as cross-domain absorption of a
neighbour's ground; and "web properties" is literally in kake's Adjacent slot of our
PROVINCE.md.

**Ruling the counter.** kake's entry scope cell disclaims the operator/researcher side
("Nothing here says what an operator-owned property serves") and teaches only publisher
delivery on GitHub Pages (Jekyll builds, HTTPS/text-plain serving, duplicate-path rule).
The seam is pre-adjudicated: `corpus/lessons/round-38.md` "Contested scope — kake's
security.txt `CSAF` mention: adjacent, reported not absorbed … the seam is a citation
rather than a move". ScoutSibling.txt (this wave) prints "Contested scope: none" — 38
kake hits, all round-35 admission artifacts; zero in every other sibling and the fleet
root. My own `grep -rliE 'security\.txt|rfc.?9116'` over `*/corpus` and `*/SKILL.md`
agrees: the only sibling admission is kake's, the only kasegi hits are passing mentions.

**Verdict 1: IN-PROVINCE.** Researcher-side disclosure-channel discovery is core kasegi
work; kake's publisher-side admission is disjoint and the seam is already ruled.
Smallest safe correction: none.

## A2 — Fetch stability of https://www.rfc-editor.org/rfc/rfc9116.txt

Two raw fetches ~7 min apart plus the seat's earlier fetch — three total, all byte-identical:

| time (UTC) | HTTP | bytes | sha256 |
|---|---|---|---|
| 2026-10-27T08:19:23Z (ExecC2Capture manifest `fetched_utc`) | 200 | 45129 | `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9` (`raw_sha256`) |
| 2026-10-27T08:21:16Z (mine #1) | 200 | 45129 | `79d19ce7…61f9` |
| 2026-10-27T08:28:04Z (mine #2) | 200 | 45129 | `79d19ce7…61f9` |

`cmp` mine#1 vs mine#2: byte-identical. Document shape: UTF-8 **with BOM** (`ef bb bf`),
LF line endings, 0 CR bytes, 0 form feeds, no pagination headers — the modern
non-paginated RFC rendering. Cross-day stability: kake's S078 retention from
2026-10-22 (`4954ddcd…`, 37916 B) differs from today's body only in normalization shape
(their copy collapses the BOM+blank header to `…Internet Eng…` line 1); the normative
text is the same — and RFCs are immutable post-publication.

**Hazard noted, mitigated in the actual manifest record:** the *served* body
(1122 lines, 45129 B) is not the committed capture (842 lines, 39301 B,
`925512e715be…`), because `capture-source.py --kind text` collapse() trims lines,
collapses runs and drops blank lines but **keeps the BOM as capture line 1**. The seat
recorded both sha256s explicitly (`raw_sha256` vs `sha256`), so the manifest pins
post-normalization bytes — B2's anchor model stays sound. Verifier rule for wave 2:
re-fetching must compare against `raw_sha256` (79d19ce7…), not the snapshot sha.

**Verdict 2: STABLE.** Byte-identical across three fetches spanning ~9 min and five days
against kake's retention; the only instability is normalization-shape, and it is declared.

## A3 — Are the three located quotes actually in the text?

Tested against the landed capture `wave1/ExecC2Capture.S063.txt` (sha `925512e7…`) using
source-recheck.py's own `normalize()` (whitespace collapse + `<u>` strip) and anchor window
(lines anchor-1..anchor+3):

| id | quote (manifest record) | occurrences | anchor | verdict |
|---|---|---|---|---|
| Q1 | `For web-based services, organizations MUST place the "security.txt" file under the "/.well-known/" path` | 1 | 330 | anchor-ok (§3, heading L329) |
| Q2 | `It is RECOMMENDED that the value of this field be less than a year into the future to avoid staleness.` | 1 | 270 | anchor-ok (§2.5.5) |
| Q3 | `When the value of this field is an email address, it is RECOMMENDED that encryption be used (as per Section 2.` …(email-encryption RECOMMENDED, §2.5.3) | 1 | 235 | anchor-ok |

Also verified in the raw text: `the one in the "/.well-known/" path MUST be used` (raw L446,
unique), `Keys MUST NOT appear in this field.` (raw L317, unique), `the file access MUST use
the "https" scheme` (raw L449).

**Trap the scribe avoided (verified):** the served text wraps `/.well-known/security.txt`
mid-token (`/.well-` + `known/security.txt`, raw L440-441) — Q1 correctly ends at
`"/.well-known/" path`, inside the wrap. Any quote spanning the wrap would fail B2.

**Verdict 3: REAL.** All three pinned quotes occur exactly once and anchor-verify on the
committed capture bytes.

## A4 — Can harness 27/27 be reached WITHOUT a real entry?

What `frontier-recheck-count.py` reads: F-rows in `corpus/README.md`
(`^\|\s*(F\d+)\s*\|…`), status cell must be exactly `admitted`; each admitted row's entry
cell resolves `root/<path>` or `root/corpus/<path>`. `evaluate()` then requires: entry
file exists (else `missing-entry`), a `source:`/`evidence` declaration set, a `recheck:`
line that is a `source-recheck.py` invocation with `--manifest` + `--source`, recheck-ids
== declared ids == subset of cited ids, manifest exists/schema-1/lists the ids — and only
then runs the recheck command at lane root, exit 0 required. Plus `DUPLICATE-ENTRY`
realpath fail-closed. Demonstrated on a git-archive mirror of `fbba3d96`:

- **Map-only edit cannot do it.** `printf '| F24 | … | admitted | knowledge/rfc-9116-security-txt.md | S063 | …\n' >> corpus/README.md` →
  `FAIL F24 knowledge/rfc-9116-security-txt.md ids=- exit=- problems=missing-entry;
  entries=27 pass=26 exit=1`. A `queued` row would escape the harness but fire the kill
  limb "status cell not `admitted`"; a duplicate entry path fires DUPLICATE-ENTRY.
- **But the whole counter chain is internally-consistent-only.** Adding a fabricated family —
  junk-bytes `S063.txt` ("JUNK BYTES NOT RFC 9116…", sha256 recorded in a fabricated
  manifest record whose single quote pins that junk text), a 4-line forged entry with
  trio + `cd <root> && source-recheck … --source S063`, a well-formed SOURCES S063 row,
  and one `knowledge-expected.txt` line — yields every frozen counter green:
  `entries=27 pass=27 exit=0` with `PASS F24 … ids=S063`; `records=55 bound=55 unbound=0`;
  `lines=60 total=60 pass=60 … expected=60 missing=0 unexpected=0 exit=0` (audit strict
  pass=60/60 after the mirror's cd-root convention fix — a mirror artifact, not a lane
  defect). The mirror's `source-recheck.py` is the lane's real instrument: junk bytes
  pass because the fabricated manifest's sha256 and quotes pin those same junk bytes.

So: no, not without an entry — the instrument's minimum is a self-consistent artifact
*family* (row + entry + manifest + capture + expected line), matching the kill rule's
"junk twin" limb which rejects only an *incomplete* family. **However, a complete forgery
reaches every printed counter; the frozen chain measures consistency, not authenticity.**
Authenticity stands on the fetch ledger + receipt provenance (three independent fetches in
A2 do corroborate this capture) and on independent re-fetch at review — the judge's
cheapest decisive check is `curl … rfc9116.txt | sha256sum` against `raw_sha256`.
Smallest safe correction (advisory, not required): have the final-gates receipt teed an
independent re-fetch line binding `raw_sha256`, converting A2's observation into an
artifact. Also noted: B2/anchors bind quotes to committed bytes, not to upstream truth —
the instrument's docstring says exactly this, so it is a stated limit, not a defect.

**Verdict 4: map-only impossible (proven); full-family forgery possible (proven on
mirror) — a real, fixable boundary: the kill rule is complete for the O4/junk-twin class
but silent for a self-consistent forged family; review must re-fetch.**

## A5 — Is tier A justified for an RFC? (arguing against tier inflation)

**Against (strongest counter).** RFC 9116 is Category **Informational** — "This document
is not an Internet Standards Track specification; it is published for informational
purposes" (raw L21-22). If tier A means "binding standards-track authority", the RFC
under-claims. S062 (OASIS CSAF v2.1, a Committee Specification *Draft* — pre-final) sits at
tier B, and S058 (OpenVEX main-ref) at B, so a B-tier lobby exists: Informational ≈
non-final authority.

**Ruling the counter.** The registry's measured convention — 51 mined rows at A; B only for
deliberately supporting/secondary or mutable/draft documents (S034 citizen explainer,
S058 mutable main ref, S062 draft monitor); C only for rejected rows (S026/S027/S081-class) —
scopes tier to *the row's scope cell*, i.e. "the issuer's own normative statement for this
document", not to standards-track force. RFC 9116 is the canonical, immutable, IETF-consensus
primary text for the format it defines; nothing else is more primary. Its Informational
status limits the *claim's reach* (it binds no deployment) and the F24 topic does not claim
otherwise — the right place to carry that limit is the scope cell wording, exactly as kake's
S078 does ("Informational track, so not a standards-track requirement"). Downgrading to B
would contradict six same-class spec rows: S055 (OASIS CSAF v2.0 os) A, S059/S060 (CycloneDX
v1.7) A, S022/S029/S030/S031/S033 (CNA rules, CRA, e-Gov statute) A — none of which are
stronger authorities than an RFC is for its own format.

**Verdict 5: TIER A JUSTIFIED.** It is the primary normative text for its scope cell; the
Informational caveat belongs in the scope wording (check the landed S063 row carries it —
kake's S078 model is the precedent), not in the tier cell. No inflation: tier A here does
not assert the RFC binds the world, only that the row cites the issuer's own statement.

## Summary of attacks

| # | attack | verdict | residual |
|---|---|---|---|
| 1 | in-province? | YES — researcher-side channel discovery; kake seam pre-ruled adjacent | none |
| 2 | fetch stable? | YES — 3 fetches byte-identical (79d19ce7…), raw vs snapshot sha declared | wave-2: re-fetch vs raw_sha256 |
| 3 | quotes present? | YES — Q1/Q2/Q3 unique + anchor-ok on committed capture | none; mid-token line-wrap avoided |
| 4 | 27/27 without real entry? | map-only NO (missing-entry, proven); forged family YES (proven) — kill rule covers incomplete twins only | reviewer re-fetch is the binding check |
| 5 | tier A for Informational RFC? | YES — A = issuer's own normative statement per measured convention | keep "Informational" in scope cell |

Net: frozen C2 survives all five attack limbs. The one substantive finding (A4) is a stated
instrument limit turned measurable: every counter went green on a forged family in a mirror —
the defence is the fetch-provenance chain (three corroborating fetches recorded above), so the
canonical judge should demand the re-fetch line land in the final-gates receipt.
