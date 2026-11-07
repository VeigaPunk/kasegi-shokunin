# Receipt 06 — independent row reconstruction + knowledge-meter recount (ExecC1Indep, 2026-11-07)

Command: `python3 $S/meter_check.py $S/base $S/after /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-93/c1/labels.tsv`
(meter_check.py is ExecC1Indep's own implementation written from the documented
resolve.py extraction rule and classification domains; no counter code imported.
Source copied to 07-meter_check-source.py.)

```
HOST mirror-present= False bounty-present= False KASEGI_MIRROR= None
== LABEL ROWS = 8
ROW OK  corpus/knowledge/citation-bases.md:14 key=claim-gates.md:3 kind=CORRECT expected==after=True unchanged
ROW OK  corpus/knowledge/citation-bases.md:14 key=ops-invariants.md:18 kind=CORRECT expected==after=True unchanged
ROW OK  corpus/knowledge/japanese-domestic-disclosure-workflow.md:7 key=japanese-domestic-disclosure-workflow.md kind=CORRECT expected==after=True unchanged
ROW OK  corpus/knowledge/triage-thresholds.md:437 key=intake-surface.md:75-76 kind=cell-repair expected==after=True cell old='`intake-surface.md:75-76` ("`reward.min` present'
ROW OK  corpus/knowledge/triage-thresholds.md:438 key=mission-control.md:37-38 kind=cell-repair expected==after=True cell old='`mission-control.md:37-38` (`openai-oauth/gpt-6-'
ROW OK  corpus/knowledge/triage-thresholds.md:454 key=SKILL.md:494-506 kind=SKILL.md:827-848 expected==after=True range SKILL.md:494-506->SKILL.md:827-848
ROW OK  corpus/knowledge/triage-thresholds.md:58 key=SKILL.md:117 kind=SKILL.md:191 expected==after=True range SKILL.md:117->SKILL.md:191
ROW OK  corpus/knowledge/triage-thresholds.md:144 key=SKILL.md:117 kind=SKILL.md:191 expected==after=True range SKILL.md:117->SKILL.md:191
METER base: resolved/total=1007/2001 gone=994 want=1007/2001 match=True
  by_class={'RESOLVES': 23, 'INTERNAL': 984, 'GONE': 994, 'MIRROR-EQUIVALENT': 0} noise_tokens=458 noise_adj_resolved/total=1007/1543
METER after: resolved/total=1009/2000 gone=991 want=1009/2000 match=True
  by_class={'RESOLVES': 23, 'INTERNAL': 986, 'GONE': 991, 'MIRROR-EQUIVALENT': 0} noise_tokens=458 noise_adj_resolved/total=1009/1542
== TOKEN-SET DIFF ==
removed:
  - [INTERNAL] SKILL.md:111
  - [INTERNAL] SKILL.md:117
  - [INTERNAL] SKILL.md:494-506
  - [GONE] intake-surface.md:75-76
  - [GONE] mission-control.md:37-38
  - [GONE] openai-oauth/gpt-6-astra:max
added:
  + [INTERNAL] SKILL.md:176-178
  + [INTERNAL] SKILL.md:191
  + [INTERNAL] SKILL.md:827-848
  + [INTERNAL] corpus/knowledge/intake-surface.md:89-93
  + [INTERNAL] corpus/knowledge/mission-control.md:55-57
class-flips: none
noise-flips: none
OVERALL PASS
```

Arithmetic: resolved -3 +5 = +2 (1007->1009); GONE -3 +0 = -3 (994->991); total -6 +5 = -1 (2001->2000).
