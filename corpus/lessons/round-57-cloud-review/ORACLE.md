# Independent oracle, frozen before candidate inspection

Reviewer: /root/judge_kasegi_round57, dispatched by integrator /root, not by author.

Primary source independently opened 2026-11-02: https://ossf.github.io/osv-schema/ (served version 1.9.2), sections Evaluation, affected[].ranges[].events Requirements, Special values; web tool references turn117view0/turn117view1. The Evaluation pseudocode makes explicit version membership and range inclusion alternatives, filters package identity first, sorts timeline events, and combines ranges existentially. Introduction includes its endpoint, fixed excludes its endpoint, last_affected includes its endpoint. BeforeLimits is existential across explicit upper bounds, with infinity when omitted. Requirements disallow multi-kind event objects and mixed fixed/last_affected in one events array, and require an introduction. Range-specific unsupported semantics are distinct from malformed containers.

Scope-derived expectations: ECOSYSTEM/GIT and prerelease/build comparisons are unknown in this intentionally bounded evaluator, unless another valid branch establishes true. Exact string membership needs no comparison engine. No testing of live targets, repository cloning, or external services is authorized or performed. All test advisories are synthetic.

The 47 expected verdicts are fixed independently in cases.json. Abstract labels map to the candidate's documented CLI labels only after the parent supplies a committed candidate hash. Invalid shapes are expected to remain distinct from could-not-evaluate. Test schema adaptation may wrap these unchanged advisory/query pairs; it may not change expected answers to match implementation. Any oracle limitation or disputed scope is reported explicitly rather than silently relaxing a failed case.

Freeze receipt is FREEZE.json. Its recorded SHA256 applies to cases.json. build_cases.py is provenance, not a command to rerun during judging (doing so would overwrite the freeze clock).
