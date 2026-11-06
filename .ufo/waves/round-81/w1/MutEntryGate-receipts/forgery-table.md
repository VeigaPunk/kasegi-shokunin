# Forgery battery: B8 (frozen) vs B8' (proposal sketch)

| forged entry | worthless because | B8 | B8' |
|---|---|---|---|
| f10_bare_no_prose.md | only pins and twelve marker lines; no Attribution/Limits/Gate sections | pass | fail |
| f11_cross_clause.md | claim k quotes clause k+3; no clause binding | pass | fail |
| f12_foreign_citations.md | fabricated "(S113.txt:999)" citations ignored wholesale | pass | fail |
| f15_overlong_span.md | 26-word verbatim span (cap is 25) | fail | fail |
| f16_repeat_one_pin.md | one pin repeated in all six claims; five pins never in a Claim | fail | fail |
| f1_boilerplate.md | six pins, one per claim, prose is lorem ipsum, rule "x" | pass | fail |
| f1b_true_provenance_boilerplate.md | same, with the manifest URL and the real access date | pass | fail |
| f2_dump_stubclaims.md | all six pins in Claim 1; Claims 2-5 carry the one-word span "the" | pass | fail |
| f3_semantic_inversion.md | pins verbatim; every claim prose asserts the opposite | pass | fail |
| f3b_true_provenance_inverted.md | as f3, with true provenance and non-empty rule text | pass | pass |
| f4_truncated_fragments.md | pins in Claim 1; Claims 2-6 cite <=25-word fragments that drop the subject | pass | fail |
| f5_paraphrase_mislocated.md | paraphrase cited on the pin's own line | fail | fail |
| f6_moved_line.md | pristine pin cited one clause off | fail | fail |
| f7_duplicate_numbering.md | six sections all numbered Claim 1 | pass | fail |
| f8_empty_markers.md | "Falsifiable rule:" and "Rejected over-generalization" with no payload | pass | fail |
| f9_fake_provenance.md | example.invalid source URL, empty access date | pass | fail |
| f13_anchor_mismatch(synthetic) | pin occurs on lines 2 and 5; manifest anchor 2, cited 5 | pass | fail |

## counter lines

- `f10_bare_no_prose.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=0 bad_marker=6 header=bad`
- `f11_cross_clause.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=6 bad_marker=6 header=bad`
- `f12_foreign_citations.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=6 bad_claim=0 bad_marker=6 header=bad`
- `f15_overlong_span.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=1 claimless=0 unpinned=1 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=1 bad_foreign=0 bad_claim=1 bad_marker=6 header=bad`
- `f16_repeat_one_pin.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=5 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=5 bad_marker=6 header=bad`
- `f1_boilerplate.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=0 bad_marker=6 header=bad`
- `f1b_true_provenance_boilerplate.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=True date=True bad_span=0 bad_foreign=0 bad_claim=0 bad_marker=6 header=ok`
- `f2_dump_stubclaims.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=11 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=6 bad_marker=6 header=bad`
- `f3_semantic_inversion.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=0 bad_marker=6 header=bad`
- `f3b_true_provenance_inverted.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=True date=True bad_span=0 bad_foreign=0 bad_claim=0 bad_marker=0 header=ok`
- `f4_truncated_fragments.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=11 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=5 bad_marker=6 header=bad`
- `f5_paraphrase_mislocated.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=6 overlong=0 claimless=0 unpinned=6 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=6 bad_foreign=0 bad_claim=6 bad_marker=6 header=bad`
- `f6_moved_line.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=1 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=1 bad_foreign=0 bad_claim=1 bad_marker=6 header=bad`
- `f7_duplicate_numbering.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=False url=False date=False bad_span=0 bad_foreign=0 bad_claim=6 bad_marker=6 header=bad`
- `f8_empty_markers.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=0 bad_marker=6 header=bad`
- `f9_fake_provenance.md` B8: `ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S115 pins=6 claims=6 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=0 bad_marker=6 header=bad`
- `f13_anchor_mismatch(synthetic)` B8: `ENTRY-GATE sid=S9 claims=1 want=1 spans=1 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok`
  B8': `ENTRY-GATE-STRICT sid=S9 pins=1 claims=1 order=True url=False date=False bad_span=0 bad_foreign=0 bad_claim=1 bad_marker=1 header=bad`
