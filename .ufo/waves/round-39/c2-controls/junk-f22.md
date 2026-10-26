# junk-f22.md — negative twin for C2 F22 (fabricated CISA When-to-Issue claims)

Control: a reader running `source-recheck.py` on a manifest carrying these four
claims against the captured `S057.txt` must get one `MISMATCH reason=quote-not-found`
per claim and exit 1 (the same instrument and shape as `c2-controls/junk-f21.md`
in round 38).

1. "CISA's When to Issue VEX Information mandates a strict protocol that determines
   when a supplier must issue VEX information." — FALSE: the document states the
   decisions and timing are primarily business decisions and are not determined by
   a strict protocol.
2. "Once a VEX status is issued it must never be changed." — FALSE: the document
   requires updating status when the investigation concludes (e.g. affected or
   not_affected), and allows timestamp-only reaffirmation.
3. "The When to Issue VEX Information document defines the five not-affected
   justification labels (component_not_present, vulnerable_code_not_present,
   vulnerable_code_not_in_execute_path, vulnerable_code_cannot_be_controlled_by_adversary,
   inline_mitigations_already_exist)." — FALSE: the labels are defined in the
   separate Minimum Requirements and Status Justifications documents; When-to-Issue
   cites them only in the inheritance discussion.
4. "CISA requires every VEX statement to include an exploitation-likelihood score,
   and its action_statement field is mandatory." — FALSE: the document says VEX
   does not specifically describe threat or the degree of exploitation, and such
   information may be included in action_statement (optional), not required.
