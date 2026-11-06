# MutEntryGate — attack on the B8 entry-content gate (Kasegi round 81, attempt 1)

Gate under test: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/c2/entry-gate.py`,
sha256 `51ee45fbd19f2efd84d107e35ebccdfd857900a5190e18d44534268c9a4d50d2` (frozen; read-only here;
every mutant and forgery ran against an exact `$S/gate.py` copy, hash equal).
Frozen inputs: S115.txt `e304eb88c7d79a6d2a1e4369c3e9a4fcf18f3ff4aabd6ad86466e85daf3f6f7f`,
round-81 manifest `7429df80bf425c8132b1325d0cd3b9e8527323f7e6eb61c31ce8b0774c5c05cf`,
draft entry `2895011e23b38deb04f634398072d70e88ce9dfe878bffe3d64d00af0c371940`.
Scratch `S=/fast/scratch/hyaku/kasegi-r81/MutEntryGate` (deleted at exit); `TMPDIR=$S` on every run.

## Verdict

1. **B8 passes the draft entry.** `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0
   overlong=0 claimless=0 unpinned=0 header=ok`, rc 0.
2. **B8 is a citation-syntax checker, not a claim-quality gate.** 13 entries built in `$S` pass
   it while carrying no verifiable claim: lorem-ipsum claims, all six pins dumped into Claim 1
   with one-word stubs elsewhere, claims that quote the pin verbatim and then assert its
   opposite, six sections all numbered `Claim 1`, empty `Falsifiable rule:`/`Rejected
   over-generalization` payloads, an invented source URL, no Attribution/Limits/Gate sections,
   a clause permutation, fabricated foreign-source citations, and a pin cited off its manifest
   anchor. Each defect names the one limb that would have to change.
3. **`--selftest` has no negative case for 26 of 32 single-transform mutants.** 32 mutants
   applied one at a time to the frozen source: 6 killed, 26 survive. A 25-case probe suite
   built here (22 negative, 3 positive) kills 21 of the 26; 5 remain, of which 3 are provably
   equivalent mutants and 2 are caught only by positive controls.
4. **Calibration: 3 pass / 91 fail over 94 (entry, manifest, source) rows and 52 manifests.**
   The 3 passes are exactly the r79–r81 entries (S113, S114, S115). 78 of 94 rows contain no
   B8-shaped span at all. B8 is correctly specified for the r79+ entry template and is
   mis-specified as a corpus-wide retrofit; it must be scoped prospectively (routed, §6).

No frozen byte was edited. Findings outside the frozen r81 claim sets are routed as round-82
defects, never verdict changes.

## 1. What B8 actually checks, verbatim from the frozen source

| limb | predicate (gate.py) | what it does not read |
|---|---|---|
| G1 header | first 8 lines contain a line starting `source: <SID> — `, a line starting `verified-at: `, and a line equal to the composed `recheck: cd <lane> …` string | the URL after the dash, the access date, whether `<lane>` is a real path or the spelling used at call time |
| G2 located | every `"<text>" (<SID>.txt:<n>)` has ≤25 words and `text in snapshot_lines[n-1]` | whether `<n>` is the manifest's `anchor` for that quote; whether the span is a whole sentence, a fragment, or contains another source's citation; elision markers (`…`) |
| G3 claims | `#Claim` sections count == manifest quote count; each has ≥1 span and a line starting `Falsifiable rule:` and one starting `Rejected over-generalization` | claim numbering, uniqueness, order, payload text (empty payloads pass), which quote a claim carries |
| G4 pinned | every manifest quote is a substring of some span inside some Claim section | that the span is the *exact* pin, that it sits under the matching clause, or that extra spans are meaningful |

Two structural consequences: a claim is satisfied by *any* span (a 1-word fragment qualifies),
and G4 only needs a pin to occur once anywhere in the claim set. Both are exploited below.

## 2. Forged entries that pass B8 and are worthless

Built against the frozen round-81 manifest; each file is preserved in
`MutEntryGate-receipts/forgery-files/` and reproduced with the gate's counter line in
`MutEntryGate-receipts/forgery-table.md`.

| forgery | passes while | why it is worthless | limb needed |
|---|---|---|---|
| f1 boilerplate | six pins, one per claim, prose `lorem ipsum`, `Falsifiable rule: x` | claims assert nothing; the rule is one letter | R4 rule payload |
| f1b true-provenance boilerplate | same, with the manifest URL and real access date | same, provenance now valid | R4 |
| f2 dump + stub claims | all six pins in Claim 1; Claims 2–5 carry only `"the" (S115.txt:36)` | four claims are a one-word quote + markers | R1 claim↔pin binding |
| f3 semantic inversion | pins verbatim, non-empty markers, prose asserts the opposite | every claim means the reverse of its quote | none lexical (see §4) |
| f3b true-provenance inversion | as f3 with real URL/date and a plausible 13-word rule | passes even the tightened B8′ | none lexical (see §4) |
| f4 truncated fragments | pins in Claim 1; Claims 2–6 cite ≤25-word fragments (`in order to construct the URL`) | the fragment drops the subject so the claim can say anything | R2 exact-span |
| f7 duplicate numbering | six sections all titled `## Claim 1` | no claim is distinguishable | R6 numbering |
| f8 empty markers | `Falsifiable rule:` and `Rejected over-generalization` with no payload | the twelve required lines are empty ritual | R4/R5 payloads |
| f9 fake provenance | `source: S115 — https://example.invalid/…`, `verified-at: ` empty | provenance is fabricated | R7 URL/date equality |
| f10 bare, no prose | only six pins + twelve marker lines; no Attribution, Limits, Distinctness or Gate section | no claim, no scope, no limits | R4/R5 |
| f11 cross-clause | claim *k* quotes clause *k+3* | claims are attached to the wrong quotes | R1 |
| f12 foreign citations | adds fabricated `(S113.txt:999)` spans | another source's citations are never parsed | R8 foreign spans |
| f13 anchor mismatch (synthetic fixture) | pin occurs on lines 2 and 5; manifest anchor is 2, entry cites 5 | the manifest's `anchor` is never cross-checked | R3 anchor |

13 passes total (12 against the frozen S115 manifest, 1 on a synthetic double-occurrence
fixture at `S/fixture/`). Four constructed vectors are **blocked** and confirm G2/G4 do real
work: f5 paraphrase cited on the pin's line (`mislocated=6`), f6 pin moved one clause
(`mislocated=1`), f15 26-word verbatim span (`overlong=1`), f16 one pin repeated six times
(`unpinned=5`).

## 3. What the gate is worth

On the 16 calibration rows whose citation syntax B8 can parse, G2 found four rows with real
content defects that no other limb sees (the rest of the row's failures are convention, §6):

- `japanese-domestic-disclosure-workflow.md` cites `"…連絡を最初に試みた日を起算日とします。" (S041.txt:340)`
  — the leading `…` is not in the capture, so the span is not verbatim (all three S041 manifests,
  identical snapshot sha `e18acbf99d13…`).
- `project-zero-fuzzilli-vs-bigsleep-comparison.md` cites `"…similar 'starting point'" (S093.txt:53)`
  and `"…overlap on 'easy' bugs" (S093.txt:90)` — the capture has curly quotes (`“starting
  point”`, `“easy”`); the entry substituted ASCII `'`. The :90 span is also 28 words.
  Both citations are unpinned, so `source-recheck.py` never saw them; only G2 catches them.

These are **routed defects for round 82** (byte-verbatim restatement, and an explicit decision
on elision), not verdict changes.

## 4. What a stricter limb would need

R1 claim↔pin binding: claim *k* must carry exactly the pin for quote *k* in manifest order
(text equality, not containment), no pin in two claims.
R2 exact span: the claim's span text must **equal** a manifest quote; containment is not
enough (kills fragments).
R3 anchor: cited line must equal the manifest `anchor` for that quote (kills the double-
occurrence case; makes the capture manifest load-bearing).
R4 rule payload: the text after `Falsifiable rule:` must be non-empty and ≥6 words (and, to
have teeth, name the line or a check).
R5 rejected payload: text after `Rejected over-generalization` must be non-empty and ≥6 words.
R6 numbering: claim numbers must be exactly 1..N in order, no duplicates.
R7 provenance: `source:` URL token must equal the manifest `url`; `verified-at` must equal the
`fetched_utc` date; the `recheck:` line should be parsed into (lane, manifest, source) and
resolved, not string-compared (the sketch implements the URL/date equality and still
string-compares `recheck:`, so item 3 of §6 remains open).
R8 foreign spans: every `(S*.txt:n)` must resolve verbatim in a capture of *that* source; today
another sid's citation is invisible.

A 100-line prototype (`receipts/drivers/gate_strict.py`, **proposal sketch, not an instrument**)
implements R1–R8. Measured:

- keeps all three real passing entries and the r81 draft entry passing (harm check, 4/4);
- kills 15 of the 16 forged entries; the per-limb counters show each new limb firing on its own
  case, independent of the shared fake header in the older fixtures: f2/f4/f11/f16 on binding
  (`bad_claim=6/5/6/5`), f7 on numbering (`order=False`), f12 on foreign spans
  (`bad_foreign=6`), f1/f1b/f8/f10 on marker payloads (`bad_marker=6`; f1b has a passing
  header), f9 on URL/date (`url=False date=False`), f13 on the anchor (`bad_claim=1`);
- **f3b survives**: quote the page verbatim and non-vacuously, then assert its opposite in the
  claim prose. No lexical rule closes this. If entailment matters, the gate must say so and
  route the claim to human/model review; a regex cannot decide it. B8's docstring should
  therefore not claim to close "claim prose" — only citation form.

## 5. Mutant analysis: the baked-in `--selftest` covers two limbs

32 single-transform mutants of the frozen gate, each byte-identical to the base except one
hunk (transform resolution asserted `count(old)==1`); full table in
`MutEntryGate-receipts/mutant-table.md`. Selftest cases: `good`/`dump`/`moved`/`norule`.

- killed by selftest (6): M03 overlong-counts-chars, M04 mislocated-off, M05 mislocated-whole-
  snapshot, M08 unpinned-join, M11 claimless-off, M12 claimless-spans-only.
- survive selftest (26). The selftest exercises exactly the mislocated limb (via `moved`) and
  the marker-presence limb (via `norule`); every other limb has no negative case.
- 21 of the 26 survivors are detected by the 25-case probe suite built here (19 by a negative
  probe, 2 only by a positive control), i.e. the gap is test-suite, not spec: header (window, dash, sid, verified-at, recheck exactness), claim count
  equality in both directions, empty spans, claim numbering, overlong, unpinned scope and
  direction, case-folding/stripping of the line match, rule/rejected anchoring.
- 5 survivors remain: M22 (claim title must contain an em dash — caught only by the positive
  `p_claim_no_dash`), M24 (`"(.+)"` span regex — caught only by `p_two_spans_on_line`),
  M25 (`re.escape(sid)` removed — equivalent for `S\d{3}` ids), M31 (`and spans` dropped —
  equivalent while a manifest has ≥1 quote), M32 (`body.split("\n## ")` removed — equivalent
  after `re.split(r"(?m)^## ")`).
- 2 mutants are additionally caught only because they break the `good` case (M03, M08), i.e.
  the positive case is load-bearing for the `overlong` and `unpinned` limbs.

Recommended `--selftest` additions, each of which kills at least one surviving mutant:
`overlong_pin` (a 26-word span containing the pin), `pins_outside_claims`, `pin_fragment_claims`,
`five_claims` / `seven_claims`, `claim_unnumbered`, `empty_span_claims`, `header_late`,
`header_dash_missing`, `verified_inline`, `recheck_suffix`, `line_zero` (n=0), `two_spans_on_line`,
`claim_no_dash` (positive), `span_padded`, `span_case_variant`. Exact fixtures are in
`MutEntryGate-receipts/forgery-files/`; base verdicts for all 25 probes are in
`MutEntryGate-receipts/probe-table.md`.

## 6. Calibration: B8 against every admitted entry that has a round manifest

Method: for each `corpus/source-snapshots/round-*/manifest.json` and each source id in it, find
every `corpus/knowledge/*.md` whose `source: <SID> ` line names that id, then run the frozen gate
with that manifest and lane. 52 manifests, 94 (entry, manifest, source) rows, 85 distinct
(entry, source) pairs (S041 appears in round-26/28/30 and S112 in round-77/78, so the same frozen
entry is judged against several quote sets). Full 94-row table:
`MutEntryGate-receipts/calibration-table.md`; summary `calibration-summary.txt`; appendix A below.

**Result: 3 pass, 91 fail.** Passes: `osv-determineversion-cc-library-versioning.md` (S113,
round-79), `osv-ubuntu-binary-to-source-mapping.md` (S114, round-80),
`osv-importfindings-record-quality-feedback.md` (S115, round-81). All three use the r79+
template: one `## Claim k` per manifest pin, exact pin text, one `Falsifiable rule:` line per
claim.

Why the other 91 fail, in the gate's own counters:

| bucket (partition of the 94 rows) | rows | reading |
|---|---|---|
| pass | 3 | S113/S114/S115, the r79+ 1:1 template |
| no B8-shaped span at all (`spans=0`) | 78 | the corpus writes citations as bare `(SID.txt:n)` (e.g. S094 `(S094.txt:18, Q1)`) or as inline quotes; B8's `"text" (SID.txt:n)` form is a r72+ convention and only 16 rows use it |
| span(s) present, claim shape only (`claims≠want`, `claimless>0`) | 9 | entries group many pins under one claim (S108: 6 claims / 31 pins; S109: 6 / 16 and no `Falsifiable rule:` lines); includes S112 round-77 (5 / 13) and round-78 (5 / 7) |
| span(s) present, plus a G2 content defect | 4 | S041 ×3 (leading `…`), S093 (2 mislocated incl. 1 overlong) |
| *(orthogonal)* rows that pass the header limb | 16 | 3 pass overall; of the 13 that fail, 9 have no B8-shaped span and 4 carry spans but fail the claim shape — the `recheck:` convention propagated ahead of the claim template |

Calibration facts that matter for the round-81 claim:

- **Header limb**: 16 rows pass G1; 13 of them still fail (9 have no B8-shaped span at all,
  4 fail the claim shape). So the header convention propagated ahead of the claim template.
- **Joint entries**: 9 entries cite 2–4 sources; 29 rows come from them. Run per single SID (as
  B8 must be), the other sources' citations are not parsed at all (f12 vector) — a joint entry
  can therefore carry fabricated citations for its other sources with impunity.
- **Manifest multiplicity**: S112's quote set narrows from 13 (round-77) to 7 (round-78); the
  same frozen entry text goes from `unpinned=6` to `unpinned=0` but still fails on the claim
  count. A later round that adds pins silently re-judges older entry bytes; B8 has no
  grandfathering rule.
- **Lane spelling**: the `recheck:` line is compared to a string built from the *call-time*
  `--lane`. Observed live: one synthetic entry flipped `header=ok → bad` when the same gate was
  invoked with a relative `--lane` and the entry named the absolute path. Equivalent spellings
  (relative, trailing slash, symlink) change the verdict; parse and resolve instead.

**Mis-specification statement.** 91/94 admitted rows fail, and 78 of them fail before the gate
reads any claim prose (no span in its syntax). A gate that fails 97% of the admitted corpus is
not detecting 91 defects; it is enforcing a template introduced at round 79. Options: (a) scope
B8 to entries whose `verified-at`/manifest round is ≥ 79 and record the 78 legacy rows as
"pre-B8 convention" (recommended; frozen bytes are never edited, and the three passes show the
template is achievable); (b) add a legacy clause for bare `(SID.txt:n)` citations, which would
be a different gate; (c) rewrite 91 frozen entries — excluded by the wave contract. This is a
routed defect for round 82, not a change to the r81 verdict.

### Routed defects for round 82 (outside the frozen r81 sets)

1. B8 is prospective-only; scope it or state the legacy carve-out (§6).
2. `manifest.quotes[].anchor` is never read by the gate (f13); S093's Q1 pin in fact occurs on
   lines 1 and 12, and S112 has two manifests with different quote sets.
3. `recheck:` string equality is lane-spelling-sensitive (§6).
4. Foreign-source citations are unparsed (f12; live in 9 joint entries).
5. Two unpinned S093 citations are not byte-verbatim (curly→ASCII quote substitution, one 28
   words) and one S041 citation carries a leading `…`; decide the elision rule (R2/R8).
6. `--selftest` needs the 16 fixtures listed in §5.

## 7. Evidence

- Gate and inputs unchanged before/after: `MutEntryGate-receipts/inputs-sha256.txt`
  (`51ee45fb…4d50d2` gate, `e304eb88…6f6f` snapshot, `7429df80…05cf` manifest, `2895011e…1940`
  draft).
- Forgeries and counter lines: `receipts/forgery-table.md`; files in `receipts/forgery-files/`.
- Probe suite (22 negative, 3 positive; all base verdicts as expected): `receipts/probe-table.md`.
- Mutants (32 rows) and the raw run: `receipts/mutant-table.md`, `receipts/drivers/mut2.out`.
- Calibration: `receipts/calibration-table.md` (94 rows), `receipts/calibration-summary.txt`.
- Drivers (scratch copies): `receipts/drivers/{calib.py,calib2.py,build_forgeries.py,probes.py,
  mut2.py,gate_strict.py}` plus their JSON receipts. `gate_strict.py` is a proposal sketch, not
  an instrument, and was never installed or run against lane bytes for a verdict.
- No lane file outside `.ufo/waves/round-81/w1/` was written; no git/jj command was run; no
  package was installed; scratch `S` deleted.

### Appendix A — full calibration table (94 rows: round, SID, entry, verdict, cause)

Cause codes: `H` header bad, `C` claim count ≠ pin count, `N` no B8-shaped span, `M` mislocated,
`O` overlong, `K` claim missing a marker, `U` unpinned.
- round-23 S018 multiparty-vulnerability-coordination.md: fail (C N U) — claims=0 want=6 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=6 h=ok
- round-23 S029 cra-manufacturer-reporting-duties.md: fail (C N U) — claims=0 want=9 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=9 h=ok
- round-23 S031 cna-assignment-and-vulnerability-rules.md: fail (C N U) — claims=0 want=10 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=10 h=ok
- round-24 S001 cvss-v4-severity-and-vector.md: fail (H C N U) — claims=0 want=4 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=4 h=bad
- round-24 S003 coordinated-disclosure-timelines.md: fail (H C N U) — claims=0 want=3 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=3 h=bad
- round-24 S006 authorization-safe-harbor-and-scope.md: fail (H C N U) — claims=0 want=3 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=3 h=bad
- round-24 S009 ai-assisted-finding-validation.md: fail (H C N U) — claims=0 want=2 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=2 h=bad
- round-24 S013 cwe-top25-2025-methodology.md: fail (H C N U) — claims=0 want=4 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=4 h=bad
- round-24 S032 authorised-testing-rules-of-engagement.md: fail (C N U) — claims=0 want=6 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=6 h=ok
- round-24 S033 statutory-authorization-and-unauthorized-access.md: fail (H C N U) — claims=0 want=8 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=8 h=bad
- round-24 S034 statutory-authorization-and-unauthorized-access.md: fail (H C N U) — claims=0 want=6 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=6 h=bad
- round-24 S035 statutory-authorization-and-unauthorized-access.md: fail (H C N U) — claims=0 want=6 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=6 h=bad
- round-25 S036 vendor-disclosure-policies-as-corpus-objects.md: fail (H C N K U) — claims=7 want=9 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=9 h=bad
- round-25 S036 vendor-disclosure-policy-commitments-crosswalk.md: fail (H C N U) — claims=0 want=9 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=9 h=bad
- round-25 S037 vendor-disclosure-policies-as-corpus-objects.md: fail (H C N K U) — claims=7 want=6 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=6 h=bad
- round-25 S038 vendor-disclosure-policies-as-corpus-objects.md: fail (H N K U) — claims=7 want=7 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=7 h=bad
- round-25 S038 vendor-disclosure-policy-commitments-crosswalk.md: fail (H C N U) — claims=0 want=7 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=7 h=bad
- round-25 S039 vendor-disclosure-policies-as-corpus-objects.md: fail (H C N K U) — claims=7 want=9 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=9 h=bad
- round-25 S039 vendor-disclosure-policy-commitments-crosswalk.md: fail (H C N U) — claims=0 want=9 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=9 h=bad
- round-25 S040 vendor-disclosure-policy-commitments-crosswalk.md: fail (H C N U) — claims=0 want=9 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=9 h=bad
- round-26 S041 iso-29147-and-30111-division-of-labour.md: fail (C N U) — claims=0 want=7 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=7 h=ok
- round-26 S041 iso-29147-divergence-and-clause-crosswalk.md: fail (C N U) — claims=0 want=7 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=7 h=ok
- round-26 S041 japanese-domestic-disclosure-workflow.md: fail (H C M U) — claims=0 want=7 spans=14 mislocated=1 overlong=0 claimless=0 unpinned=7 h=bad
- round-26 S041 japanese-severity-vocabulary-and-impact-model.md: fail (H C N U) — claims=0 want=7 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=7 h=bad
- round-28 S041 iso-29147-and-30111-division-of-labour.md: fail (H C N U) — claims=0 want=6 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=6 h=bad
- round-28 S041 iso-29147-divergence-and-clause-crosswalk.md: fail (H C N U) — claims=0 want=6 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=6 h=bad
- round-28 S041 japanese-domestic-disclosure-workflow.md: fail (H C M U) — claims=0 want=6 spans=14 mislocated=1 overlong=0 claimless=0 unpinned=6 h=bad
- round-28 S041 japanese-severity-vocabulary-and-impact-model.md: fail (H C N U) — claims=0 want=6 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=6 h=bad
- round-28 S042 japanese-domestic-disclosure-workflow.md: fail (H C U) — claims=0 want=6 spans=16 mislocated=0 overlong=0 claimless=0 unpinned=6 h=bad
- round-29 S043 program-severity-ladders-and-reward-scales.md: fail (H C N U) — claims=0 want=4 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=4 h=bad
- round-29 S044 program-severity-ladders-and-reward-scales.md: fail (H C N U) — claims=0 want=4 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=4 h=bad
- round-29 S045 program-severity-ladders-and-reward-scales.md: fail (H C N U) — claims=0 want=4 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=4 h=bad
- round-30 S046 japanese-severity-vocabulary-and-impact-model.md: fail (H C N U) — claims=0 want=4 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=4 h=bad
- round-30 S047 japanese-severity-vocabulary-and-impact-model.md: fail (H C N U) — claims=0 want=5 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=5 h=bad
- round-30 S041 iso-29147-and-30111-division-of-labour.md: fail (H C N U) — claims=0 want=3 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=3 h=bad
- round-30 S041 iso-29147-divergence-and-clause-crosswalk.md: fail (H C N U) — claims=0 want=3 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=3 h=bad
- round-30 S041 japanese-domestic-disclosure-workflow.md: fail (H C M U) — claims=0 want=3 spans=14 mislocated=1 overlong=0 claimless=0 unpinned=3 h=bad
- round-30 S041 japanese-severity-vocabulary-and-impact-model.md: fail (H C N U) — claims=0 want=3 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=3 h=bad
- round-31 S048 vendor-third-party-finding-coordination.md: fail (H C N K U) — claims=2 want=11 spans=0 mislocated=0 overlong=0 claimless=2 unpinned=11 h=bad
- round-32 S049 chinese-crowdsourced-testing-scope-and-rewards.md: fail (H C N K U) — claims=6 want=8 spans=0 mislocated=0 overlong=0 claimless=6 unpinned=8 h=bad
- round-32 S050 chinese-crowdsourced-testing-scope-and-rewards.md: fail (H N K U) — claims=6 want=6 spans=0 mislocated=0 overlong=0 claimless=6 unpinned=6 h=bad
- round-34 S051 immunefi-vscs-v2-2-smart-contract-severity.md: fail (H C N K U) — claims=7 want=18 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=18 h=bad
- round-35 S052 cisa-kev-catalog.md: fail (H C N K U) — claims=6 want=5 spans=0 mislocated=0 overlong=0 claimless=6 unpinned=5 h=bad
- round-36 S053 epss-exploit-prediction-scoring.md: fail (H C N K U) — claims=6 want=4 spans=0 mislocated=0 overlong=0 claimless=6 unpinned=4 h=bad
- round-37 S054 ssvc-stakeholder-specific-vulnerability-categorization.md: fail (H N K U) — claims=4 want=4 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=4 h=bad
- round-38 S055 csaf-vex-product-status-and-justifications.md: fail (H C N K U) — claims=7 want=4 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=4 h=bad
- round-39 S057 cisa-when-to-issue-vex.md: fail (H C N K U) — claims=10 want=4 spans=0 mislocated=0 overlong=0 claimless=10 unpinned=4 h=bad
- round-40 S016 anthropic-cvd-provenance-and-pacing.md: fail (H C N K U) — claims=5 want=3 spans=0 mislocated=0 overlong=0 claimless=5 unpinned=3 h=bad
- round-40 S017 pz-reporting-transparency-trial.md: fail (H C N K U) — claims=5 want=3 spans=0 mislocated=0 overlong=0 claimless=5 unpinned=3 h=bad
- round-40 S019 nist-sp800-216-vdp-framework.md: fail (H C N K U) — claims=6 want=3 spans=0 mislocated=0 overlong=0 claimless=6 unpinned=3 h=bad
- round-40 S020 doj-vdp-framework-scope-and-authorization.md: fail (H C N K U) — claims=8 want=1 spans=0 mislocated=0 overlong=0 claimless=8 unpinned=1 h=bad
- round-40 S021 cisa-bod-20-01-vdp-minimums.md: fail (H C N K U) — claims=9 want=1 spans=0 mislocated=0 overlong=0 claimless=9 unpinned=1 h=bad
- round-40 S023 cisa-cvd-program-stages.md: fail (H C N K U) — claims=7 want=2 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=2 h=bad
- round-40 S025 cve-bench-agent-exploitation-benchmark.md: fail (H C N K U) — claims=8 want=2 spans=0 mislocated=0 overlong=0 claimless=8 unpinned=2 h=bad
- round-40 S060 cyclonedx-analysis-subtree.md: fail (H C N K U) — claims=7 want=3 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=3 h=bad
- round-41 S063 rfc-9116-security-txt.md: fail (H C N K U) — claims=7 want=3 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=3 h=bad
- round-42 S064 cve-json-record-format.md: fail (H C N K U) — claims=7 want=4 spans=0 mislocated=0 overlong=0 claimless=7 unpinned=4 h=bad
- round-43 S067 claim-package-gate.md: fail (H C N U) — claims=0 want=6 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=6 h=bad
- round-44 S069 google-cloud-vrp-customer-resource-boundary.md: fail (H C N U) — claims=0 want=5 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=5 h=bad
- round-45 S071 linux-kernel-security-bugs-reporting-process.md: fail (H C N U) — claims=0 want=30 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=30 h=bad
- round-46 S073 github-private-vulnerability-reporting.md: fail (H C N U) — claims=0 want=8 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=8 h=bad
- round-47 S075 zdi-disclosure-policy.md: fail (H C N U) — claims=0 want=10 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=10 h=bad
- round-47 S076 github-repository-security-advisories.md: fail (H C N U) — claims=0 want=12 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=12 h=bad
- round-49 S078 cve-services-publication-api.md: fail (H C N U) — claims=0 want=8 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=8 h=bad
- round-50 S080 osv-affected-range-events.md: fail (H C K U) — claims=5 want=16 spans=1 mislocated=0 overlong=0 claimless=5 unpinned=15 h=bad
- round-51 S081 cisa-vulnrichment-adp-enrichment.md: fail (H C N K U) — claims=4 want=12 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=12 h=bad
- round-52 S083 nvd-api-2.0-retrieval-interface.md: fail (H C N K U) — claims=4 want=12 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=12 h=bad
- round-53 S085 nvd-api-2.0-response-schema.md: fail (H C N K U) — claims=4 want=13 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=13 h=bad
- round-54 S086 openssf-scorecard-checks.md: fail (H C N K U) — claims=4 want=14 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=14 h=bad
- round-55 S087 github-repository-security-advisories-rest-api.md: fail (H C N K U) — claims=4 want=14 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=14 h=bad
- round-56 S088 cisa-vulnrichment-record-list.md: fail (H C N K U) — claims=4 want=6 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=6 h=bad
- round-57 S089 iso-29147-30111-standard-records.md: fail (H C N K U) — claims=4 want=7 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=7 h=bad
- round-57 S090 iso-29147-30111-standard-records.md: fail (H C N K U) — claims=4 want=7 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=7 h=bad
- round-58 S091 aisi-autonomous-cyber-capability-progress-rate.md: fail (H C K U) — claims=4 want=9 spans=2 mislocated=0 overlong=0 claimless=4 unpinned=9 h=bad
- round-59 S092 google-big-sleep-findings-tracker.md: fail (H C N K U) — claims=4 want=10 spans=0 mislocated=0 overlong=0 claimless=4 unpinned=10 h=bad
- round-60 S093 project-zero-fuzzilli-vs-bigsleep-comparison.md: fail (H C M O K U) — claims=4 want=15 spans=10 mislocated=2 overlong=1 claimless=4 unpinned=15 h=bad
- round-61 S094 project-zero-big-sleep-sqlite-variant-analysis.md: fail (C N K U) — claims=3 want=7 spans=0 mislocated=0 overlong=0 claimless=3 unpinned=7 h=ok
- round-62 S095 cert-guide-cvd-phases-and-validation.md: fail (C N U) — claims=0 want=19 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=19 h=ok
- round-65 S098 first-psirt-services-framework.md: fail (C N U) — claims=0 want=18 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=18 h=ok
- round-67 S100 first-psirt-maturity-document.md: fail (H C N U) — claims=0 want=48 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=48 h=bad
- round-67 S101 first-psirt-maturity-document.md: fail (H C N U) — claims=0 want=10 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=10 h=bad
- round-68 S102 openssf-scorecard-api-contract.md: fail (H C N U) — claims=0 want=8 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=8 h=bad
- round-69 S103 github-global-security-advisories-rest-api.md: fail (H C N U) — claims=0 want=13 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=13 h=bad
- round-70 S105 github-advisory-database-curation-semantics.md: fail (H C N U) — claims=0 want=19 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=19 h=bad
- round-71 S106 zdi-disclosure-process-and-vendor-coordination.md: fail (H C N U) — claims=0 want=15 spans=0 mislocated=0 overlong=0 claimless=0 unpinned=15 h=bad
- round-72 S107 bugzilla-rest-api-bug-endpoints.md: fail (C K U) — claims=5 want=17 spans=25 mislocated=0 overlong=0 claimless=5 unpinned=3 h=ok
- round-73 S108 osv-post-v1-query-contract.md: fail (C U) — claims=6 want=31 spans=23 mislocated=0 overlong=0 claimless=0 unpinned=10 h=ok
- round-74 S109 fuzzilli-js-engine-fuzzing-framework.md: fail (C K U) — claims=6 want=16 spans=51 mislocated=0 overlong=0 claimless=6 unpinned=14 h=ok
- round-75 S110 fuzzilli-ndss2023-jit-fuzzing-paper.md: fail (H C K U) — claims=3 want=24 spans=24 mislocated=0 overlong=0 claimless=3 unpinned=6 h=bad
- round-77 S112 osv-post-batch-query-contract.md: fail (H C U) — claims=5 want=13 spans=10 mislocated=0 overlong=0 claimless=0 unpinned=6 h=bad
- round-78 S112 osv-post-batch-query-contract.md: fail (C) — claims=5 want=7 spans=10 mislocated=0 overlong=0 claimless=0 unpinned=0 h=ok
- round-79 S113 osv-determineversion-cc-library-versioning.md: **pass**
- round-80 S114 osv-ubuntu-binary-to-source-mapping.md: **pass**
- round-81 S115 osv-importfindings-record-quality-feedback.md: **pass**
