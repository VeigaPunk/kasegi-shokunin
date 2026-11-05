# CISA Vulnrichment published record list — the catalog surface of CISA's ADP record publication: the 28 per-year record folders 1999-2026 with no gap, the six non-record support entries beside them, the content-addressed completeness pin, and the README blob whose round-51 snapshot still reproduces

source: S088 — https://api.github.com/repos/cisagov/vulnrichment/git/trees/develop — capture corpus/source-snapshots/round-56/S088.txt (1 line, 7204 snapshot bytes over 7203 fetched bytes; sha256 09ce0b10436f67c35f7ccf3a8dcfec0489d209d6698ee2fa75cf4b6f5873935e; recorded fetch 2026-11-01T14:34:05Z, HTTP 200 — byte-identical across four same-sha instrument opens this round: probe 14:19:12Z, recorded 14:34:05Z, verification second and third opens 14:34:05Z/14:34:06Z; one raw curl open served the SAME tree object pretty-printed at 8956 bytes and parses equal — controls/s088-opens-r56.txt); manifest corpus/source-snapshots/round-56/manifest.json (6 assertions Q1-Q6, each occurrences=1 at anchor line 1)
verified-at: 2026-11-01 (opened this round; the tree object is content-addressed and the develop ref is mutable — the pinned top sha e8d691a5d5b8485339feb29aac2d68deb67f2011 is the open-time authority; the 90d row recheck re-fetches and a moved ref reads a different object by construction)
ground: F37
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && (python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-56/manifest.json --source S088 || python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-56/manifest.json --source S088)   # interpreter-portable form (run from the lane root, no `cd` prefix); prints S088:sha256 OK then one S088:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

GitHub's own git-trees machine interface, read at CISA's Vulnrichment repository default ref: the
served tree object is the machine form of the published record list — what the program publishes
and how the publication is organized, stated by the repository's own structure (Q6 names the
object's content address). The records' CONTENT is not in this capture: a top-level tree lists
names, types and blob sizes only. This entry is documentation-only — it instructs no call against
any CVE record, no probing, scanning or submission against any target, and carries no credential
material.

## Claim 1 — the published record list is a per-year directory family with no gap: 1999 through 2026

The record folders are the 28 year directories 1999–2026: the first entry pinned at
`"path":"1999","mode":"040000","type":"tree"` (S088.txt:1, Q1), the last at
`"path":"2026","mode":"040000","type":"tree","sha":"a10553f66cc32bd05eb8f5be93ad626c9161f100"`
(S088.txt:1, Q2), and the year-form count re-derives from the capture:
`grep -oE '"path":"(19|20)[0-9]{2}","mode":"040000","type":"tree"' | wc -l` → 28 = 2026−1999+1.
Falsifiable rule: a record folder named outside the four-digit year form, or a missing year inside
the span, is outside this publication's declared organization. Rejected over-generalization: the
year folders' contents (the per-CVE ADP record JSON) are NOT asserted by this capture — a
top-level tree lists no descendants; the record format stays F25/S064 ground.

## Claim 2 — the list is served as one content-addressed, self-declared-complete object

The served object names its own content address (S088.txt:1, Q6: `{"sha":"e8d691a5…","url"`) and
closes with `"truncated":false` (S088.txt:1, Q5) — the API's own completeness claim for this
listing; the entry count re-derives: 34 entries = 30 tree-type + 4 blob-type
(`grep -c '"mode"'` over the capture → 34). Falsifiable rule: `"truncated":true`, a different
entry count, or a different top sha at a later re-open of the same ref is a DIFFERENT list state —
the pin is the arbiter, not the URL. Rejected over-generalization: byte-stability holds per
representation only — the same tree object serialized compact (7203 bytes to this instrument) and
pretty-printed (8956 bytes to curl's `*/*` Accept) differs at byte level while parsing equal
(the receipt's parsed-equality limb); nothing here asserts any serialization is stable across
calls.

## Claim 3 — the rules text CISA teaches from sits in the list as one 8501-byte README blob, and the round-51 capture still reproduces

The list carries `"path":"README.md","mode":"100644","type":"blob","sha":"ce41a364…","size":8501`
(S088.txt:1, Q3) — the same raw byte count the round-51 open recorded (the S081 row's provenance:
8501 raw bytes), and the committed S081 snapshot sha256 2da09414… reproduces byte-identically from
a same-day raw fetch of the README after the declared collapse normalization
(controls/s088-opens-r56.txt, final limb: collapsed sha == committed sha == 2da09414…).
Falsifiable rule — this is the check on F32's scope limit: the enrichment RULES live in
README.md (and the flowcharts file it links), not in the record list; a future open whose
snapshot sha does NOT reproduce means the F32 entry's taught rules have drifted, and its 90d
recheck re-derives from the new bytes. Rejected over-generalizations: the reproduction is a
same-day observation, not a cross-round stability assertion; the raw README at the mutable ref
served 163 raw lines this day while the collapsed text is what reproduces — the raw-byte form is
NOT pinned by this check, only the snapshot normalization is.

## Claim 4 — the record list carries support surfaces beside the records, named as such

Beside the 28 record folders the list names exactly six non-record entries: the support trees
.github and assets, and four blobs — CONTRIBUTING.md (2400 bytes), LICENSE (7048), README.md
(8501) and flowcharts.md (3916) (S088.txt:1, Q4 pins the flowcharts entry). The program's own
README marks the flowcharts as process description, not enrichment data: "These flowcharts
illustrate the Vulnrichment process. Please note that the details in the flowcharts are subject
to change as Vulnrichment processes are refined." (S081.txt:9 — the round-51 capture, reproduced
this round by Claim 3's check). Falsifiable rule: a reader treating flowcharts.md as ADP
enrichment data contradicts the program's own README line. Rejected over-generalizations: the
flowchart DETAILS are unasserted here (the README itself declares them changeable; the SSVC
framework ground stays F20/S054); and the list ranks and describes nothing — a tree carries no
per-record metadata, so no claim about WHICH CVEs are enriched is available from this surface at
all.

## Distinctness

- vs F32/S081 (the enrichment program's data rules): that is WHAT CISA writes into ADP containers
  and when it yields; this is the publication LIST — the catalog surface (what exists, how
  organized) read through the repository's machine interface. The S081 ground is unchanged by
  this row; the same-day reproduction check (Claim 3) is corroboration, not a rewrite.
- vs F25/S064 (the CVE record format): the per-record JSON structure is not in this capture and
  is not asserted; the tree names folders, not record schemas.
- vs F30/S078 (CVE Services publication interface): that is the CVE Program's write path; this is
  CISA's repo-side catalog read through GitHub's git-trees interface — different service,
  read-only, no submission semantics.
- vs F20/S054 (the SSVC framework): flowcharts.md is NAMED by this list, its content unasserted;
  the framework ground stays F20.

## Limits

One tree object at one instant, read-only: the develop ref is mutable and the pinned top sha
e8d691a5… is the open-time authority — a later open of the same URL after a sync reads a
different object by construction, and the 90d row recheck re-fetches. The response body is
Accept-negotiation-dependent (compact 7203 vs pretty-printed 8956 bytes for the same object):
byte-stability is asserted per representation only. The year folders' contents (the per-CVE ADP
records), the sync cadence, the commit history, rate limits and authentication are unasserted.
The GitHub releases variant of this surface was probed and is EMPTY (the releases atom feed
carries no entries; GET /releases returns `[]`) — recorded in the round-56 hunt bullet as the
lead's negative probe, so no release-list ground is claimable. No call was made against any CVE
record or CISA service beyond this public tree read; the capture is a catalog, and
submission/testing remains refused by the province.
