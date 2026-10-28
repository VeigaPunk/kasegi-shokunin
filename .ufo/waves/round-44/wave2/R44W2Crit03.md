# R44W2Crit03 — overgeneralization attack on F26 (round 44, wave 2, falsify)

- seat: R44W2Crit03 (leaf, falsify wave; no delegation, no background work)
- date: 2026-10-28
- target: `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` @ commit `8063547d0ce647d6f9eafc3c8d0a502616685218`
- item: report any sentence stating a GENERAL authorization, scope or reward rule rather than the Google Cloud VRP's own boundary; test whether the entry keeps the Cloud VRP boundary distinct from general authorization and from customer permission.

## Verdict

**Not falsified.** No sentence in the entry states a general authorization, scope, or reward rule as the entry's own assertion. Every normative sentence is one of: a quoted Cloud VRP rule (every anchor verified against the pinned capture), an explicit disclaimer of generality, a package instruction conditioned on the Cloud VRP context, or an explicit rejection of the very over-generalization this attack tests. The entry keeps the Cloud VRP boundary distinct both from general authorization and from customer permission.

## Method and provenance checks

1. Drift check: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat 8063547d0ce647d6f9eafc3c8d0a502616685218 -- corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md corpus/source-snapshots/round-44/S069.txt corpus/source-snapshots/round-44/manifest.json` → empty output, exit 0. No working-tree drift; all line citations below are valid for both the committed tree and the working tree.
2. Capture digest: `git -C <lane> show 8063547d…:corpus/source-snapshots/round-44/S069.txt | sha256sum` → `0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2`, 45,681 bytes, 1,132 lines — byte-identical to the sha256 pinned in `corpus/source-snapshots/round-44/manifest.json` and in the S069 registry row (`corpus/SOURCES.md:75`, tier A). Provenance chain closed: every quoted sentence below was read from the committed bytes.
3. Word-count claim (entry:28, "21 words"): `printf '%s' "Finding a Google-owned asset inside a customer IP block during a broad scan is still considered unauthorized testing within customer space." | wc -w` → 21. Confirmed.

## Quote-anchor verification (all passed)

| entry line | quoted text | cited | observed in S069.txt |
|---|---|---|---|
| 9, 15 | "product or web service that handles reasonably sensitive user data is intended to be in scope" | 10-11 | exact across L10-11 (sentence begins L9: "In principle, any [Google Cloud]…") |
| 11 | "The Google Cloud VRP scope is strictly limited to Google-owned infrastructure and services" | 61-62 | exact across L61-62 |
| 11 | "To protect customer data and privacy, testing customer resources is strictly prohibited" | 62-63 | exact across L62-63 |
| 11 | customer domains `*.bc.googleusercontent.com`, `*.appspot.com` as "examples" | 68-69 | L68-69; source says "include, but are not limited to", so "examples" is faithful |
| 17 | "the report is ineligible for a reward if finding or verifying it involved testing or accessing customer resources" | 70-72 | exact across L70-72 |
| 22 | written-authorization prohibition + ineligibility | 65-72 | L65-67 (prohibition) and L70-72 (ineligibility) |
| 28, 32 | "Finding a Google-owned asset inside a customer IP block during a broad scan is still considered unauthorized testing within customer space" | 76-77 | exact across L76-77; 21 words |
| 28 | multi-tenant escapes: local reproduction instead of live testing | 78-87 | L78-87 (full bullet) |
| 18 (table) | same multi-tenant rule | 78-86 | range ends mid-sentence (bullet runs 78-87); cited content lies inside the range — immaterial |

Manifest Q1-Q5 anchors (61, 62, 70, 76, 10) match their quotes. Entry:3's "captured through the official article API" matches the manifest `capture_url` (`https://bughunters.google.com/rest/v1/articles/about/rules/google-friends/cloud-vulnerability-reward-program-rules`, HTTP 200).

## Line-by-line overgeneralization scan

- :3-5 — provenance and recheck pointer only; no rule content.
- :9 — first sentence explicitly disclaims generality: "it is not a rule for Google's other programs or a general authorization opinion." The trailing instruction narrows ("Read that as a program scope statement, not permission to test an arbitrary Google-branded or customer-owned service") — restrictive, not general.
- :11 — all three sentences are the VRP's own boundary or a narrowing gloss ("the suffix alone is a reason to inspect the program's ownership boundary, not proof that a target is Google-owned").
- :13-18 (table) — every package consequence is a restriction or a bookkeeping instruction: "do not generalize this to Google Workspace or other programs" (:15); "Do not represent customer-hosted resources as authorized Cloud VRP targets" (:16); "Record reward-ineligibility separately from the technical validity of a finding; do not erase the finding or imply permission" (:17); "Keep the package's evidence bounded to the local reproduction and analysis; do not test a live shared tenant" (:18). None grants anything.
- :22 — Limits disclaims generality three ways ("not general law, a statement about all Google programs, or proof of authorization for any action") and keeps customer authorization and Cloud VRP reward eligibility explicitly separate, attributing both rules to S069:65-72 rather than adopting them as the entry's own grants.
- :26 — names four general principles held by other entries (F03/F09/F13/F01) and disclaims them as "shared principles, not F26's expansion"; all four cross-references verified (below). This is the sentence most at risk of reading as a general rule; it attributes instead of asserts.
- :28 — the derived ground ("customer IP-range ownership remains the boundary even when an individual asset is Google-owned") is introduced as the Cloud VRP's "program-specific, previously uncovered restriction" and is tied to the verified S069:76-77 quote.
- :30 — the falsifiable rule is conditioned on "when a report claims a Cloud VRP target is eligible" and ends in a prohibition ("do not treat a Google-owned asset inside it as permission to scan or test").
- :32 — explicitly rejects the over-generalization ("A Google-owned asset is in scope even when it lies inside a customer IP range") and pins the re-open condition to a change in Google's Cloud VRP rule itself.
- :36 — disambiguates the S069 token collision with round-35's separate namespace; verified (below).

## Distinctness verdict (the item's second question)

- vs **general authorization**: kept distinct at :9 (explicit disclaimer), :22 ("not general law…"), :26 (general principles attributed to other entries, not claimed here), :30 (conditioned on a Cloud VRP eligibility claim, and prohibitive). The registry row itself carries the same boundary ("not a universal authorization rule", `corpus/SOURCES.md:75`; index line `corpus/SOURCES.md:86`).
- vs **customer permission**: kept distinct at :17 ("do not … imply permission"), :22 ("Customer authorization and Cloud VRP reward eligibility are separate"), :30 (a customer-owned address range is "do not treat … as permission"). The source's written-authorization clause (S069.txt:65-67) is attributed to the program's prohibition, never converted into a grant by the entry.

## Cross-references verified (entry:26, :36) — all accurate

- F03 `corpus/knowledge/authorization-safe-harbor-and-scope.md:8` — "A safe-harbor badge or statement alone does not add assets to scope or establish permission for an action that the program's policy excludes." matches "distinguishes policy scope from a safe-harbor badge".
- F09 `corpus/knowledge/statutory-authorization-and-unauthorized-access.md:46` — "the platform's text cannot supply that third party's consent, however broad its wording" matches.
- F13 `corpus/knowledge/program-severity-ladders-and-reward-scales.md:16` — program-controlled vs third-party assets; and :18 of that entry carries the same anti-general close ("bounds in this policy record, not a general cap formula for other HackerOne programs or other platforms").
- F01 `corpus/knowledge/cvss-v4-severity-and-vector.md:34` — "Keep the report's technical score and vector distinct from the program's own severity, eligibility, and reward criteria." matches.
- `corpus/lessons/round-35.md:124,136-139` — S069 there is the `kass.sacinfo.org.cn` national-standard PDF in a separate namespace with a transport caveat ("later reader must not treat the fetch as clean"); the entry's collision note is accurate and necessary.

## Nits (recorded; none rises to the attack)

1. :9 (and the same fragment at :15) quotes only S069.txt:10-11 and drops the source's opening "In principle, any [Google Cloud]" (S069.txt:9). The elision is under-inclusive — the source sentence is broader and hedged — so it is not overgeneralization; but the entry never tells its reader that the scope statement is hedged "In principle" and opens with "any Google Cloud".
2. :18 (table row 4) cites S069.txt:78-86 where the multi-tenant bullet runs 78-87; the cited content lies inside the range, so the one-line-short citation is immaterial.

## Could not falsify / limitations

- I could not produce a single sentence that states a general authorization, scope, or reward rule as the entry's own claim. F26 survives this attack on the committed tree.
- I verified the committed pinned capture, not live-site equality: the registry note (`corpus/SOURCES.md:154`) itself records that the live API later returned formatting differences and that the digest is the dated capture. I did not re-run `source-recheck.py` against the network; this was an offline, read-only attack.
- Out of scope for this seat (not checked): the F26 frontier row in `corpus/README.md`, C2's counting predicates, and the C1 counter — those belong to other seats' items.

## Discipline and tooling record

- This seat edited only its own Report path (this file). No production file, no other seat's file, no git/jj mutation, no fleet-repo or sibling-lane writes. Scratch `/fast/scratch/hyaku/kasegi-r44/R44W2Crit03/` (S069.txt, manifest.json) removed before yield.
- No tool installed or upgraded: the committed bytes were read with git read-only commands plus `sha256sum`, `wc`, `printf` (coreutils already present). Reason: nothing beyond what was present was needed. Pacman untouched.
