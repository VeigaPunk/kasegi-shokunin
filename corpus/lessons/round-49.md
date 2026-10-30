# Round 49 — citation-base grounding and the CVE Services publication surface

Two declared claims, both frozen before any seat scored: C1 on depth:verifiability (the lane's lowest
non-retired axis, score 4) and C2 on coverage (frontier admission F30). Base
`9b1662a2fa0e7c7b0ad6c4d45cb7786f27bdd03b`; freeze commit `1954022d91c2063d0ce25bb5551778bc0b3e70f3`;
claim file `.ufo/waves/round-49/claims.json`; do-nothing control
`.ufo/waves/round-49/controls/do-nothing.txt`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| stale instrument census quoted as current | the committed census of record `corpus/instruments/citation-survival.md` described "Scope: `SKILL.md` + `corpus/**/*.md` (50 files)" and a lane rate of 134/1480 = 9.05%, while the base tree held 228 corpus markdown files and the live instrument run at the base commit read 1071/4696 = 22.81% — a 13.8-point gap between the number the lane had been quoting and the number its own instrument produced on the same tree | none; no lane criterion requires an instrument's census file to be regenerated before a round quotes it, and the axis rows quote the file | the round regenerates the census at the base commit **before** the freeze and commits it (the freeze commit `1954022d` carries the live census: 4696 distinct citations, 1071 in the numerator). Shown able to fail: the two files disagree on the same tree — the stale file's own rate lines and the regenerated file's rate lines are both in the tree history, and the round-49 report quotes the regenerated ones. |
| counter defect found by its own self-test before the freeze | the first implementation of `corpus/instruments/citation-ground-check.py` compared site tokens by substring (so the old token `knowledge/entry.md` counted as "still present" inside the repaired `corpus/knowledge/entry.md`) and its self-test fixture placed the lane outside the fleet root, so the fleet-relative class could never fire; three of ten self-test cases failed on that code | QUALITY R50 (a counter is freeze-ready only after a pre-freeze mutant battery) and R53 (both attack classes), applied to the counter's own fixtures | exact whole-token comparison at every site, and the fixture tree now nests the lane inside the fleet root. Shown able to fail: the frozen bytes' self-test reports `selftest cases=10 failures=0`, and the round-49 wave's mutation seats re-introduce each defect in a scratch copy and read the matching case red. |
| a past verdict read as a standing ban | `corpus/README.md:702` (the round-47 note) reads "No F30 row is admitted: the proposed ZDI timeline frontier duplicates F02's existing coordinator/trigger/interval discipline" — a verdict on the ZDI candidate, but readable as a prohibition on any F30 row | none; the lane's append-only style keeps superseded verdicts in place without a pointer to what they decided | the round-49 README amendment names the round-47 sentence as the round-47 verdict on ZDI and states that the round-49 F30 is a different surface (the CVE Program's write path), so the two readings cannot be confused. |
| claim written before its measurement existed | the round report's C1 section stated that the isolated effect of the repair had been measured on two scratch exports (the landed tree and the same tree with the repair reversed); the two exports were deleted while their census runs were still in flight, and the runs then failed with `FileNotFoundError` (exit 1, `/fast/scratch/hyaku/r49-after-tree.log`) while the reversed-tree run produced no output at all — the measurement was never taken | none; the evidence standard says a command offered as evidence is a re-run performed at write time, and the round wrote the sentence before the run finished | the report's sentence is withdrawn by an appended erratum that states what WAS measured (the whole-tree census difference between two commits plus the counter-derived merge arithmetic) and what was not (the isolated effect), and the claim's predicate is re-stated as resting on the frozen counter alone. A measurement sentence may not be written before its run has produced an output. |
| the lane's own base vocabulary had no entry for the fleet root | `corpus/knowledge/citation-bases.md` names LANE, MIRROR, ORIGIN-WORK, LOST-TREE, LOST-BASE and BLOB-PIN, but not the fleet repo that holds PROTOCOL.md, MISSION.md, `.ufo/` and the sibling lane repos; 11 citations written fleet-root-relative therefore had no base to be read against | none; the vocabulary is complete only for the bases the lane happened to use | the vocabulary gains a FLEET base entry (round 49) and the fleet-root-relative class is repaired to absolute fleet paths; the residue that the lane may not edit is enumerated (79 members in protected files) and named as debt rather than left implicit. |

## Gate

**S078 admitted** — CVE Services API, OpenAPI 3.0.2, `info.version` 2.8.8.1, first-party (the CVE Program's
own repository), kind `spec`, tier A, status `mined`, opened 2026-10-30, recheck `90d`, used-by
`corpus/knowledge/cve-services-publication-api.md`. URL
`https://raw.githubusercontent.com/CVEProject/cve-services/master/api-docs/openapi.json`; capture
`corpus/source-snapshots/round-49/S078.txt` (sha256 `1403e607cf2c5be529b9d34bad5f1ebe6b72c7673fb1de2fda79431bf1684472`,
282553 bytes, 8374 lines), manifest `corpus/source-snapshots/round-49/manifest.json` (8 assertions Q1–Q8,
each exactly-once at its pinned anchor; `source-recheck.py --source S078` exits 0).

Located quote grounding `teaches` (17 words by `wc -w`): "Reserves CVE IDs for the organization provided in
the short_name query parameter (accessible to CNAs and Secretariat)" (S078.txt:125). The four further
anchors the entry cites: S078.txt:6 (the service description, 18 words), S078.txt:1368 (CNA-container
create, 17 words), S078.txt:1798 (ADP-container update, 17 words), S078.txt:5285 (conversation create, 15
words) and S078.txt:6354 (the organization header, 11 words).

**Admitted:** the CVE Services publication surface as frontier row F30 — the write path (identifier
reservation, CNA-container publication and update, rejection, ADP-container enrichment, CNA↔Secretariat
conversation), admitted on the lane's own coverage map with a first-party capture, a knowledge entry whose
`recheck:` line re-verifies its own declared source, and a registry row whose URL binds to the capture.

**Rejected, with reason and flip:** the round-48 Bugcrowd researcher-reporting lead stays rejected — its
guessed dispute route returned HTTP 404 in round 48, the lane holds no coverage-map ground for a
platform-mediated dispute flow, and the round-49 critic seat R49Crit02 was asked to attack the CVE Services
admission instead. Flip condition: a first-party capture of the platform's report-and-dispute surface that
documents the workflow itself. The staged campaign package
`/home/vgpnk/Projects/shokuknow/merge/kasegi/` was **not** adopted this round: the round-48 read-only
id-collision screen showed mass id drift between the package's older registry baseline and this lane's
registry, so no staged row is appendable without wholesale renumbering; the package also holds no
citation-base or CVE Services ground.

**Spot-check:** the round's gate decisions (admit S078 / admit F30; refuse the Bugcrowd lead as the rejected
row S079; refuse the staged package) have **no independent non-author spot-check**. The outside check that
exists (`corpus/lessons/round-48-verifier-spotcheck.md`) covers the prior round, not this one.

**Wave disposition — validated, released UN-DISPATCHED.** The round built and validated its falsification arm
and the operator released it undispatched: the 64-seat wave-1 spec (`.ufo/waves/round-49/wave1-spec.json`,
policy v2, band 64-128, 64 spawn seats, 31 of them attack roles) and its rendered dispatch
(`wave1-dispatch.json`) were committed and the ready file (`wave1.ready`, written 13:02) was taken by the
lane's own hand, but the operator's wrap-up ruling released the wave **without spawning a single seat** (the
same ruling as SoujiR45 r45). No seat ran, no seat report exists, no `wave1-results.json` was written and no
WAVE-DONE message was received. This round therefore claims **no falsification credit from wave 1**: the
two claims verify on their frozen predicates by re-derivable commands, and the round's independent
non-author verification duty remains outstanding.

## Limits

- The C1 counter grades citation shape and path resolvability, not the truth of a citation's claim. It
  cannot tell whether a repaired path is the referent the sentence means; that judgment is per row, written
  in the ledger's referent note, and attacked by the wave's reviewer seats and by the labrat probe that plants
  a wrong-referent row.
- The 68 repairs are class-complete only over the lane's own files. 79 further class members sit in
  `round-*-verifier-spotcheck.md` and `round-*-aggregator-*.md` lessons, which the lane may not edit; they
  are enumerated and disclosed as debt, and a reader still cannot open those citations.
- One repaired row carries a pre-existing anchor drift: `/home/vgpnk/Projects/shokunin/MISSION.md:49-56`
(fleet MISSION.md) held the
  push-scope allow-list at round 15 and the fleet file's push scope now begins at line 81. The repair keeps
  the file and the historical anchor and records the drift in the ledger's referent note; the anchor was not
  silently rewritten.
- The wave that was to falsify this round never ran; the round's admission rests on the frozen predicates
  alone, which is why the report states the honest stop rather than an admitted round.
- The C2 capture is one release of one document. The recheck verifies the pinned bytes and the located
  quotes; it does not claim that the live service still behaves this way, and the entry claims nothing about
  request bodies, rate limits or error codes.
