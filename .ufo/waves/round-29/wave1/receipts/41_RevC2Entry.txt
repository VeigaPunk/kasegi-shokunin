# F13 entry bar-check — RevC2Entry

**Verdict: disagree with admission of the final entry reviewed.** I re-opened the full 58-line entry after it landed. Most substance is present and attribution, falsifiability, and documentation-only constraints are handled well; remaining concrete bar failures are Q8 and Q10. The assigned source-id equality and foreign-cwd checks pass.

## Q1–Q10

| Criterion | Agree / disagree | Evidence |
|---|---|---|
| Q1 | Agree | Under the title: three `source:` lines each name S-id, URL and anchor/JSON location, followed by `verified-at:` and a runnable `recheck:` command. |
| Q2 | Agree | Load-bearing claims are tied to tier-A S043/S044/S045, with opened captures and manifest assertions. |
| Q3 | Agree | Claim-bearing sections contain verbatim source excerpts with exact policy sections, capture lines, or JSON paths and manifest Q identifiers; quotes are within the 25-word rule except the displayed scale list, which is a short table transcription explicitly anchored to manifest Q4. |
| Q4 | Agree | The entry repeatedly attributes the policy/taxonomy/crosswalk to HackerOne or Bugcrowd and explicitly says these are not universal rules. |
| Q5 | Agree | Three falsifiable checks are stated; two over-generalizations are rejected with source-grounded reasons. |
| Q6 | Agree | The entry is documentation-only and contains no target-action instructions or credential/session/private-URL material. |
| Q7 | Agree | Recheck is executable source-recheck invocations, not prose; the named manifest provides pinned-source checks. (The missing/corrupted-source control was not run in this review.) |
| Q8 | Disagree | The entry does not declare the required normalization or identify a receipt naming the applied transformation (`normalized=markup-whitespace`). It cites manifest Q ids, but the manifest's purpose statement alone does not name the transformation. |
| Q9 | Agree | Source ids/path stems bind in the manifest; every assertion has quote/location and the recheck prints occurrence counts. Caveat: S043 assertions have repeated normalized text (12 occurrences); their explicit `anchor: 1` is required and present. |
| Q10 | Disagree | The line is one command with `cd <lane-root> &&`, but it lacks the required human note after `#` and the foreign-cwd `bash -n` check reported `bash_n_exit=0`; the syntax requirement passes, while Q10's complete form is not met because no note is included. |

## Assigned end-to-end checks

1. **Capture anchors / exactly-once quotes — agree with pin checks, with S043 anchors.** Re-opened manifest and snapshots. `source-recheck.py` for each of S043/S044/S045 exited 0. S043 Q1–Q4 observed counts were 12, 12, 1, 12; each has `anchor: 1`, and the instrument printed `anchor=1-ok`. S044's four assertions and S045's four assertions each printed `occurrences=1`. Entry claims cite these manifest assertions; S043's duplicate occurrences are explicitly disclosed in the entry's limits, not misrepresented as exactly-once.
2. **Foreign-cwd recheck and `bash -n` — agree on execution.** Executed the full entry command from `/tmp`: `bash -n` exit 0 and run exit 0. All three ids reported SHA-256 OK and quotes passed, with counts above.
3. **`--source` set equals declared `source:` set — agree.** Declared ids are `{S043,S044,S045}`; the command selects exactly those three ids in three chained invocations; sets equal.

## Q4, Q5, Q6 substantive review

- **Q4 attribution:** agree. HackerOne standard-policy limits are scoped to that record; Bugcrowd VRT baseline and its override remain Bugcrowd-attributed; the CWE mapping observations are scoped to the captured Bugcrowd dataset. The entry expressly rejects universalizing these policies/scales.
- **Q5:** agree. Rules/checks 1–3 are falsifiable against pinned material. Rejected claims (“P1–P5 is universal” and “null means no CWE exists”) each include why the cited platform-specific source does not support that generalization.
- **Q6:** agree. No probing, scanning, login, or submission directions appear.

## Refused candidate spot-check

Re-opened read-only package candidate `knowledge/corpus/knowledge/program-scope-rules-and-asset-boundaries.md`. **Agree with its refusal** as recorded in round-28 gate: its statement “Three different mechanisms, one invariant” and “the authorization to test is owned by the asset owner, and every platform's scope list is a restatement of that ownership” generalizes across HackerOne, CNVD, and 360SRC from those platforms' own statements. That is the precise Q4 failure: source-specific platform policy is converted into a universal rule. The candidate's opening also says “A bug-bounty program cannot authorise anything it does not control,” while the cited sources are platform policy pages, not a universal legal/authorization authority. The refusal's concern is supported by the reopened candidate text. This spot-check does not independently reopen the staged CNVD/360 source captures.

## Residual risk / verification gaps

The review's Q10 disagreement is a narrow form issue (missing `#` human note), despite successful foreign-cwd execution and `bash -n`. Q8 remains a substantive documentary omission: state the actual normalization and receipt evidence in the entry. The refusal review did not verify its Chinese-source citations. No changes to the entry were made by this reviewer.