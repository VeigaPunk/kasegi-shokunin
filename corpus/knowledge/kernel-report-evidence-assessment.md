source: S090 — https://docs.kernel.org/process/security-bugs.html, Preparing your report / What qualifies as a security bug / Responsible use of AI; capture corpus/source-snapshots/round-58/S090.txt
verified-at: 2026-11-02
recheck: cd /workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S090

# Kernel report evidence assessment — F27 executable deepening

## Policy-specific judgment

The kernel maintainers require a stable upstream version, problem description with manifestation evidence, a reproducer with trigger and confirmation, and relevant conditions. Their text anchors this in “A stable identifier” (S090:74) and “both a way to trigger” (S090:86). Binary-only evidence and time-relative versions fail those requirements. Recent-code verification matters; a dated observation alone does not establish present relevance.

A reproducible bug is not automatically a security-list issue: examine whether it “crosses a trust boundary” (S090:132), on a correctly configured production system, and assess urgency/exploitability separately. Do not invent impact from a crash or from polished prose.

AI assistance is not blanket rejection. It changes public handling; “do not publicly share a reproducer” (S090:138) accompanies the instruction to mention availability. Report quality and public-reproducer handling are separate decisions. This is kernel-specific guidance, not a universal bounty-program rule.

## Replayable training, not real report acceptance

Run `python3 corpus/instruments/kernel-report-assess.py .ufo/waves/round-58/example.json` from the lane root. Full input grammar is frozen in `.ufo/waves/round-58/CONTRACT.md`. The specimen is a deliberately invented owner-only ACL over an imaginary record. No kernel is touched, and input strings are never executed. A buggy model permits a guest read; a fixed model denies it; an owner read is legitimate. This establishes only the toy's behavior.

The evaluator binds the selected trace to declared version, conditions, trigger and confirmation, then independently replays its toy specimen. A forged reproduced flag cannot substitute for replay. The caller's expected permission must match the toy policy. All-fields-present reports can still yield needs-evidence or an unestablished boundary. Run `python3 corpus/instruments/kernel-report-check.py` to replay the frozen pairs.

| Paired evidence | Bounded judgment |
|---|---|
| Guest, buggy model, matching context | Corroborated synthetic behavior; toy boundary supported |
| Same report, fixed specimen but old granted trace | Replay contradicts trace; needs evidence |
| Fixed specimen with accurately denied trace | Corroborated observation, no boundary crossing |
| Owner legitimately reads, claim says owner was forbidden | Claim contradicts the model's authority; boundary unestablished |
| Same complete report, wrong trace version or conditions | Context binding fails; field presence is irrelevant |
| AI report with annotated public reproducer block | Withhold reproducer regardless of evidence judgment |

## Human review checklist and hard limits

1. Re-open the project's current policy before real-world use; pinned-source recheck is not a live refresh.
2. Independently authenticate and reproduce actual evidence in an authorized environment. This tool neither does that nor grants authority to do it.
3. Review source provenance, exact affected range, recent-tree correspondence, dependencies and configuration. The tool only recognizes a narrow identifier syntax, not all valid kernel revisions.
4. Evaluate the actual kernel threat model, permissions, trust boundary, reachability and urgency. The toy cannot stand in for any of them.
5. Inspect the complete proposed public text manually. Block kinds are caller annotations; this is not a semantic leak detector. A reproducer mislabeled summary is a disclosed blind spot, not safe output.
6. Keep submission, contact, authorization, severity and rewards outside the probe. Exit 0 means assessment completed, never report accepted.

Rejected over-generalization: matching structured evidence proves a valid kernel security report. Even matching invented data establishes no authenticity, production configuration or kernel exploitability. Rejected substitute source S091 is useful for stack-trace debugging, not sufficient authority for this security-intake/AI handling judgment; its rejection is scoped, not a claim that debugging guidance is false.
