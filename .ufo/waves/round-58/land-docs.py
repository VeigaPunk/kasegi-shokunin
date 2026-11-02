# One-shot author construction record; DO NOT rerun on landed tree.
import pathlib,json
root=pathlib.Path('.')
def append(p,s):
 with pathlib.Path(p).open('a') as f:f.write('\n'+s.strip()+'\n')
p=pathlib.Path('corpus/SOURCES.md');text=p.read_text();lines=text.splitlines(keepends=True);at=max(i for i,l in enumerate(lines) if l.startswith('| S089 |'))+1
rows='''| S090 | Linux kernel security bugs — https://docs.kernel.org/process/security-bugs.html | docs | A | Kernel-specific report evidence and AI public-reproducer handling | Preparing your report / What qualifies / Responsible use of AI; capture 2026-11-02 S090.txt:74,86,132,138 | Deepens S071: stable upstream identity and reproducible evidence are distinct from public handling and security qualification | mined | 2026-11-02 | 90d | corpus/knowledge/kernel-report-evidence-assessment.md |
| S091 | Linux kernel Bug hunting — https://docs.kernel.org/admin-guide/bug-hunting.html | docs | A | General kernel stack-trace debugging, not security-intake policy | Bug hunting introduction; capture 2026-11-02 S091.txt:76 | REJECTED: stack-trace debugging alone does not establish security-report sufficiency or AI disclosure handling; flip: explicit relevant security-intake clauses | rejected | 2026-11-02 | 90d | — |
'''
lines.insert(at,rows);p.write_text(''.join(lines))
append('corpus/SOURCES.md','Round-58 bounded source search (2026-11-02): question: how to distinguish supported report evidence from polished fields and AI disclosure handling? Identified/screened 2 official pages, included 1 (S090), excluded 1 as insufficient policy authority (S091). Both opened with the same capture instrument, HTTP 200. No old status/recheck/used-by cells changed. S090 deepens S071 rather than replacing its historical source. Stop: operative policy located and paired offline evidence tests established; no target research.')
p=pathlib.Path('corpus/instruments/knowledge-expected.txt');names=p.read_text().splitlines();print('expected before',len(names));names.append('corpus/knowledge/kernel-report-evidence-assessment.md');p.write_text('\n'.join(sorted(names))+'\n');print('expected after',len(names))
append('corpus/README.md','''## Round-58 F27 deepening — synthetic evidence judgment (2026-11-02)

| Area | Entry | Source basis |
|---|---|---|
| Kernel report evidence assessment; executable deepening of existing F27, NOT a new numbered frontier | knowledge/kernel-report-evidence-assessment.md | S090 — official policy reopened; S091 scoped rejected alternative |

The original F27 reporting-process entry remains historical source-bound knowledge. This addition contributes a replayable synthetic assessment with explicit evidence/authority/disclosure separations. No recovered root, additional lost-domain surface or generic report acceptance is claimed.''')
append('PROVINCE.md','''[r58 F27 deepening, 2026-11-02] `corpus/knowledge/kernel-report-evidence-assessment.md` and `corpus/instruments/kernel-report-assess.py` add bounded synthetic report judgment to existing kernel reporting ground. The ACL replay is a teaching model, not kernel testing. No new numbered frontier or source-root restoration; live-target testing and submission remain refused. Research methods remain chousa-owned; secret handling remains kagi-owned.''')
append('SKILL.md','''## Round-58 kernel-report evidence judgment

Trigger: reviewing kernel-specific report evidence or AI-public handling. Anti-trigger: real-target testing, submission, or generic report-validity certification. S090 and `corpus/knowledge/kernel-report-evidence-assessment.md` deepen F27; full schema and limits: `.ufo/waves/round-58/CONTRACT.md`.

| Evidence situation | Decision discipline |
|---|---|
| All required fields exist but selected trace belongs to another version/configuration | Needs evidence; presence does not bind the observation |
| Claimed reproduced flag contradicts the harmless replay | Needs evidence; retain contradiction |
| Owner is legitimately allowed; report calls the same action forbidden | Boundary claim unestablished, not a supported security finding |
| Guest receives invented record under buggy toy policy | Toy-only crossing; never infer kernel validity, urgency or severity |
| AI-assisted finding, public text includes annotated reproducer | Withhold that reproducer, regardless of evidence completeness |
| AI-assisted finding, status-only public text | Separate handling rule, not blanket rejection of AI findings |

Checklist: verify stable upstream identity and recent-code check; match version/conditions/trigger/confirmation; replay the harmless specimen; distinguish legitimate authority from a crossing; keep public-reproducer handling independent; inspect unannotated prose manually. Any actual report still needs authenticated reproduction and kernel threat-model review outside this tool. Never execute supplied strings. Exact identifier syntax is deliberately narrow; caller declarations are not externally verified.

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| kernel-report-assess.py | probe | `python3 corpus/instruments/kernel-report-assess.py INPUT.json` | 0 assessment completed, NOT clean/accepted; 2 invalid or unsupported could-not-evaluate | paired CLI harness below | .ufo/waves/round-58/CONTRACT.md | reads supplied JSON only; no payload execution/network | kasegi |
| kernel-report-check.py | gate | `python3 corpus/instruments/kernel-report-check.py` | 0 clean expected decisions; 1 mismatch; 2 unavailable/tampered could-not-evaluate | `python3 corpus/instruments/kernel-report-check.py --selftest` | .ufo/waves/round-58/fixtures.json digest in freeze.json | temporary synthetic JSON only, removed | kasegi |

Error patterns and counterexamples: `.ufo/waves/round-58/mutations.py` challenges actual evidence/boundary/disclosure decisions, not issue-word presence. Public block labels are annotations, not a free-text leak detector. The toy is not a security simulator or an exploit.''')
