# ScoutF15Sweep — negative sweep for F15 ground (round 31, wave 1)

Question: does the lane already hold "vendor as finder / vendor research programme as an intake route
for OTHER vendors' bugs"? Read-only. No lane file edited except this receipt. No network. Tooling installed: none.
All paths relative to /home/vgpnk/Projects/shokunin/kasegi-shokunin. Sweep ran 2026-10-25 on the tree as found
(other seats were editing; no counter was run, so no PRE-STATE comparison is made).

## VERDICT: `residual-exists` (narrow — two of the three MSVR routes have a partial lane analogue; one residual is wholly new)

## Sweep (command + output)

Scope S = `corpus/knowledge/*.md corpus/README.md corpus/SOURCES.md SKILL.md` (43 knowledge files).
Command per term: `grep -n -i -c -- "$t" $S | grep -v ':0$'` (case-insensitive, files with hits only):

| term | hits (file:count) |
|---|---|
| MSVR | none |
| MSRC | none |
| Microsoft | knowledge/submitted-registry.md:1 (L198 `microsoft-bounty-family`, a submission-registry directory name, not this topic) |
| third-party | authorization-safe-harbor-and-scope.md:1 (third-party *asset ownership*, L39); operator-queue.md:1 (program text); program-severity-ladders-and-reward-scales.md:1 (HackerOne third-party *assets*); vendor-disclosure-policies-as-corpus-objects.md:1 (Cybozu scope L33); vendor-disclosure-policy-commitments-crosswalk.md:3 (L23 Cybozu scope, L52 Cisco "third-party software vulnerability… high profile", L94); SOURCES.md:2 (S020 DOJ; S040 "its named third-party coordination centres") |
| finder | cra-manufacturer-reporting-duties.md:1; iso-29147-divergence-and-clause-crosswalk.md:3 (credit-to-finder); japanese-domestic-disclosure-workflow.md:8 (JP 発見者 = reporter); multiparty-vulnerability-coordination.md:3 (L8, L25, L28 — finder as *reporter*); SOURCES.md:1 |
| coordinator of vulnerabilities | none |
| multi-vendor | vendor-disclosure-policies-as-corpus-objects.md:1 (L160, Hitachi) |
| multiparty | multiparty-vulnerability-coordination.md:1; README.md:2 (L45 row, L207 F06); SOURCES.md:1 (S018) |
| intake route | SOURCES.md:1 (S036 Cybozu, "its intake routes") |
| CERT/CC | coordinated-disclosure-timelines 5; iso-29147-and-30111-division-of-labour 6; iso-29147-divergence 4; japanese-domestic-disclosure-workflow 13; japanese-severity-vocabulary 3; policies-as-corpus-objects 4; commitments-crosswalk 7; README.md 4; SOURCES.md 7 |
| (SKILL.md, every term) | 0 hits for all ten terms |

Widened sweep (whole lane tree minus round-31 workspace): `grep -rn -i 'msvr\|msrc\|Microsoft' . | grep -v '^./.ufo/waves/round-31\|^./.git/\|^./.jj'`
→ only (a) `knowledge/submitted-registry.md:198` (b) snapshots `round-24/S002,S011,S012,S032`, `round-28/S042` (Microsoft as a named
vendor in unrelated captures: IPA monthly Microsoft-patch list, product lists), (c) `round-25/S039.txt:601,603` and `round-26/S041.txt:2091-2092`
(bibliography URLs `…/msrc/faqs-report-an-issue`, `…/msrc/cvd` — link lines only, no MSRC content captured), and (d) corpus/lessons/round-28.md:162-174,
round-28-verifier-spotcheck.md:75, round-29.md:140 — the lane's own REFUSAL of the staged package entry
`vendor-third-party-finding-coordination-2026-10-23.md` (`ground: F20` named no lane row — `grep -cE '\| F20 ' corpus/README.md` → 0; sole source staged S080 not a registry row; no located quote; prose recheck).
`grep -c 'S04[3-9]' corpus/SOURCES.md` → 12 (registry present through S047; F14 is the last admitted frontier row: README.md:284, :289 "14/14").
Further term probes (all knowledge+README+SKILL): `other vendors|another vendor|他社|他のベンダ` → only multiparty:29 (FIRST quote), crosswalk:49, policies-as-corpus-objects:159-162 (Hitachi);
`research programme|research program|vendor research|security research team` → no hits.

Conclusion of the sweep: MSVR/MSRC/"coordinator of vulnerabilities" are absent from every knowledge entry, README and SKILL.md. The topic is held only
through three adjacent entries (below).

## What each neighbouring entry already holds

1. `knowledge/multiparty-vulnerability-coordination.md` (F06, S018 FIRST v1.1). Generic roles: coordinator is an *optional third-party participant*
   ("Optional participant that can assist vendors and finders…", L25); finder = the *reporter*; upstream/downstream vendors; "publication of fixes can
   disclose the presence of the same vulnerability in other vendors' components" (L29). Holds: roles/worksheet rule. Does NOT hold: any vendor that
   itself occupies the finder or coordinator role for other vendors' products; no vendor programme object.
2. `knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (F10, S040 Cisco + Japanese vendors). Cisco row `cisco-jpcert-partner` (S040 L185-L193,
   "Incidents that may impact other vendors"): a report **received by Cisco** that "may impact multiple vendors" is routed to CERT/CC, CERT-FI, JP-CERT or NPSA;
   Cisco assists the reporter or contacts the centre on the reporter's behalf. Holds: vendor-as-*recipient* handing a multi-vendor report OUT to an
   external coordinator (inbound external report → outbound handover). Also `cisco-high-profile-bullet` (L309): a declared *third-party software*
   vulnerability is a Cisco expedite trigger. Does NOT hold: a vendor that coordinates itself, or that goes looking in other vendors' products.
3. `knowledge/vendor-disclosure-policies-as-corpus-objects.md` (F10, S039 Hitachi HIRT-PUB10008) Claim 7 (L154-L162; S039.txt:506): Hitachi's
   *own product-development flow* sometimes discovers a vulnerability; if it "affects other companies' products" (他社製品に影響する) it reports to
   the partnership's 届出窓口 and coordinated remediation starts, with multi-vendor publication aligned (S039:519). This is the closest existing
   "vendor as finder of other vendors' bugs" ground: vendor-internal discovery → spills to other vendors → handed to the national coordinator
   (IPA/JPCERT partnership). Holds: internal-discovery route, as a *side effect* of the vendor's own product QA, with the coordinator external.
   Also Cybozu row (S036:19) holds "intake is a policy-level list, bounty is one channel" — a general intake-route-list idea for the vendor's
   own products.
4. Not holding anything relevant: `coordinated-disclosure-timelines.md` (CERT/CC 90-day clock facts), `japanese-domestic-disclosure-workflow.md`
   (finder = reporter to IPA), ISO 29147/30111 entries (generic roles), `cra-manufacturer-reporting-duties.md` (finder = independent reporter).

## The exact residual a Microsoft MSVR entry would add

[Basis: the staged paraphrase at /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md
(read-only) and SOURCES.append.md:56. The MSVR page itself is NOT in the lane yet (S048 not captured at the time of this sweep) — everything about
what MSVR "states" is [INFERENCE] from the package paraphrase until a lane capture with a located ≤25-word quote exists.]

The staged claim is that MSVR learns of third-party-product vulnerabilities by (r1) Microsoft engineers finding them in third-party software in ordinary work,
(r2) external reports to MSRC where the reporter believes the issue affects a Microsoft product AND a third party (or both), (r3) internal research projects;
that MSVR itself coordinates the resulting issue; and that it names its roles as affected vendor / finder in third-party products / coordinator of
vulnerabilities affecting multiple vendors.

Against the lane's existing ground:
- r2 (external report at the vendor, multi-vendor impact) — **already held in shape by Cisco S040 L185-L193** (report received by vendor, multi-vendor, handed to coordination centres). Difference only: Cisco hands OUT to a third-party centre; MSVR states it coordinates itself. So r2 alone would be a **restatement**.
- r1 (internal engineers) — **partially held by Hitachi S039:506** (internal development finding that affects others → partnership). Difference: Hitachi's is a side-effect of QA of Hitachi products with a hand-off to an external coordinator; r1 is deliberate work in third-party software by a vendor's engineers, with the vendor coordinating. Mostly new, shares the "internal discovery" shape.
- r3 (internal research projects as an intake route) — **not held anywhere** (`research programme` probes → none).
- **Self-declared coordinator role** (vendor = "coordinator of vulnerabilities that affect multiple vendors", the vendor's own coordination of third-party findings) — **not held**. The lane's model (F06 S018, F10 Cisco/Hitachi) always places the coordinator outside the vendor (CERT/CC, JPCERT/CC, IPA, NPSA); F06 even says to "record whether one exists rather than inventing one". A vendor that is simultaneously finder and coordinator is a role-combination the F06 worksheet rule has no row for.
- **Programme-as-standing-object for the finder side** — F10's thesis is "a vendor's published policy is a standing first-party statement" about its OWN products' handling; no row treats a vendor's published programme about OTHERS' products as a corpus object. This is the F15 frontier row's natural thesis.

Exact residual (statable as one falsifiable rule): *a vendor-run programme that finds/receives/coordinates vulnerabilities in other vendors' products, with
the vendor itself occupying finder and coordinator roles, and an internal-research route (r3) — a role combination F06's worksheet and F10's
inbound-report/outbound-handover rows cannot express.* Suggested falsifiable local check for the entry: given a synthetic finding in a third party's
product reported to a vendor's response centre, require the package to record (i) which of the programme's routes it arrived by, (ii) whether the
vendor or an external centre coordinates (Cisco-style vs MSVR-style), (iii) the affected-vendor-vs-third-party split; reject a worksheet with one undifferentiated "vendor" row (extends F06's own check).

## Cautions for ExecEntryF15 / ExecCapManifest (from the refusal history; these are the traps)
1. Do NOT adopt the staged text's `ground: F20`, S080, or its prose `recheck:`; the lane refused those in rounds 28-29 (Q2, Q3, Q7/Q10, ground). Lane id is F15 / S048; cite the lane capture with an `occurrences=1` located quote.
2. The staged "Why it matters" says the *finder also has a coordinated-disclosure obligation*. That is an inference not stated in the paraphrased page; an entry must not assert an obligation unless a located quote says so (F06 Limits already: best practice, not a mandate).
3. The staged claim "lane's Cisco entry already showed … CERT/CC, CERT-FI, JP-CERT or NPSA" is true (S040 L187-L190) — cite the lane's own rows (crosswalk `cisco-jpcert-partner`; policies-as-corpus-objects Claim 7 for Hitachi) rather than the package. Expansion-credit therefore depends on foregrounding r3 + the self-coordinator role; an entry that centres on r2 collapses to a restatement of the Cisco row (CORPUS.md rule 4 / LEARNING.md expansion).
4. The lane holds no MSRC content (only bibliography URLs at S039:601,603 and S041:2091-2092); nothing in-lane supports any claim about MSRC's CVD policy, bounty, or coordination agreements — keep the staged "honest limit" (agreements not published).
5. Pre-existing counts to preserve: registry S001–S047 (12 hits for `S04[3-9]` rows), F14 the last frontier row, README.md:289 "14/14 admitted" will need the 15/15 successor line by ScribeReadmeF15.

## Reproduce
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && for t in MSVR MSRC Microsoft third-party finder 'coordinator of vulnerabilities' multi-vendor multiparty 'intake route' 'CERT/CC'; do echo "== $t"; grep -n -i -c -- "$t" corpus/knowledge/*.md corpus/README.md corpus/SOURCES.md SKILL.md | grep -v ':0$'; done`
`sed -n 506p corpus/source-snapshots/round-25/S039.txt` (Hitachi 他社製品に影響…届出窓口); `sed -n 183,195p corpus/source-snapshots/round-25/S040.txt` (Cisco "Incidents that may impact other vendors").
