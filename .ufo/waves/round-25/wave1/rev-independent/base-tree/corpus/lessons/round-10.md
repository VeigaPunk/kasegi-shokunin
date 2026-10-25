# Lessons — round 10

1. **Generated indexes have blind spots by construction.** `claim-index.mjs`
   builds the operator queue from `claims/*/*/status.json` + `claim-ready/*`
   tags, nothing else. Anything outside those two inputs — `claim-hold/*`
   tags, `vdp-disclosures/`, `submit/BLOCKED-*.md` — is invisible to it. When
   a doc says "generated deterministically", audit the generator's input set
   before trusting the output set.
2. **Tag namespaces are not self-enforcing.** Nine `claim-hold/*` tags exist
   and mean nothing to the tooling that would need to honor them. If a
   convention has no consumer in code, treat it as a note to a human, not a
   gate — and check whether the human-visible surface (the index) silently
   contradicts it.
3. **Route URLs masquerade as receipts.** `submitted_url` containing a
   landing/`reports/new` URL is field-shape misuse, not evidence of
   submission. The `/reports/<id>` discriminator plus `submission_state`
   text is the reliable tell; 9/12 queued rows carry the trap.
4. **Duplicate fingerprints must be cross-store.** The anthropic collision
   was invisible until the claim package and the VDP disclosure were
   fingerprinted side-by-side — commit + file + captured-source sha256 +
   CWE all byte-identical. A duplicate scan scoped to one directory cannot
   find a duplicate filed through a different lane.
5. **Residual gates live in `claim_checklist.md`, not in `status.json`.**
   `claimable:true` + `state:DONE` means gates pass; it does NOT mean the
   finding is submission-ready. Personio's program-OOS-mandated takeover
   proof and beanstalk's deployed-bytecode check are checklist-level facts
   that the status file never mentions.
