# Post-review oracle custody

2026-11-02: parent requested release of the pre-answer-blinded synthetic test expectations for durability after final review. Originals were found intact, not reconstructed:

- `/workspace/scratch/e2fdad13233f/private-review/kasegi59/oracle.json`
- `/workspace/scratch/e2fdad13233f/private-review/kasegi59/supplemental-oracle.json`

Their bytes contain synthetic expected metric values, brief task-specific source rationales, public source anchors and frozen test metadata. No secrets, private user information, internal instructions or private deliberative transcript is included. Pre-answer privacy was solely test blinding.

Copies in this directory are byte-identical, checked with `cmp`, with SHA256 matching their original freeze receipts:

- `initial-oracle.json`: `5658ec57f1f7f90b26b5bfb8d7ef8bc6af87c54dab71fac281ed14bbe5333bb1`
- `supplemental-oracle.json`: `e692e93dd086c3f95f06624997aae49de24d6150de7ab5559d22787d0b09bada`

Original timestamps remain embedded unchanged; this copy is post-review, not new pre-answer evidence. Original paths remain intact. Shared-filesystem blinding was procedural, not access-control isolation.

IMPORTANT: the initial oracle intentionally remains the original DEFECTIVE oracle. Its K59-10 PR:L expectation and assertion that no ambiguity was known were superseded by the review finding, not silently repaired. Use `../first-pass-review.md` and `../final-review.md` for the adjudicated result: 49 supported initial judgments plus one unsupported prerequisite inference; original C1 rejected. Supplemental results remain post-feedback learning, not rescue. Oracle release changes no score or judgment.
