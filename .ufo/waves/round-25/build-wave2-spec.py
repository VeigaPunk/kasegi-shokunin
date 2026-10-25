import json,os
L='/home/vgpnk/Projects/shokunin/kasegi-shokunin'; W='.ufo/waves/round-25/wave2'
roles=['reviewer','critic','mutation-tester','scout']
items=[]
attacks=[
('C1FrozenPredicate','reviewer','Independently re-run C1 before/frozen-after/final-after counters; verify same instrument digest and report exact receipts.'),
('C1DegenerateControl','critic','Attack the frozen three limbs with true, false, syntax-error, nonexistent-cd and own-file controls; say which pass strict.'),
('C1StrictMutations','mutation-tester','Mutate each strict limb individually on a scratch copy; each mutation must change a control result.'),
('C1CompletenessMutation','mutation-tester','Delete one recheck line and prove completeness rule fails; also test empty corpus/knowledge.'),
('C1SemanticsAudit','reviewer','Re-check 37 entry rechecks; classify executes/gated/broken and verify no fail-closed test was removed.'),
('C1CwdReplay','scout','Run every final recheck from / and lane root; compare status and output digest.'),
('C1AnchorcheckDefect','critic','Verify the reported anchorcheck exit semantics and count of fail-closed lines with no citation check.'),
('C1SourceHarness','reviewer','Run frontier-recheck-count.py; verify 12/12 and source-id binding for F10.'),
('C1InstrumentDigest','reviewer','Recompute final instrument digest and compare it with each C1 receipt/index.'),
('C1NoHarmDensity','reviewer','Re-run density.py SKILL.md and anchorcheck.py; compare against ScoutNoHarm baseline.'),
('C1LineNumberIntegrity','scout','Verify the 29 edits are one-line-for-one-line and no cited line number moved.'),
('C1AxisVerdict','critic','Adversarially assess whether C1 is depth:verifiability or operability; recommend score move/hold under R7.'),
('C2RegistryCensus','reviewer','Re-run registry census; verify 40 rows, schema, exactly two pre-existing W04s, exit 0.'),
('C2FrontierCount','reviewer','Re-run frozen frontier and new-row counters; verify 10 and 2.'),
('C2CoverageGround','critic','Try to falsify F10 as new coverage ground from the base corpus; cite any exact overlapping entry.'),
('C2ProvinceScope','critic','Adversarially check both admitted entries against PROVINCE Core and Q1-Q6, including the two-entry scope.'),
('C2S036Quote','reviewer','Re-open S036 capture and verify all entry quotes exactly once and located.'),
('C2S037Quote','reviewer','Re-open S037 capture; verify quotes and absence of invitation-only claim.'),
('C2S038Quote','reviewer','Re-open S038; ensure the legal-action quote includes its subject and no safe-harbour overclaim.'),
('C2S039Quote','reviewer','Re-open S039; verify crosswalk and JP entry quote bindings, ISO/CERT/CVE statements.'),
('C2S040Quote','reviewer','Re-open S040; verify four expedite bullets, no 30111, no-bounty claim absent, exact quotes.'),
('C2ManifestIntegrity','reviewer','Validate manifest schema, 5 pins, quote uniqueness, all source-recheck invocations, corrupt-quote control.'),
('C2EntryGateJP','critic','Try to falsify JP entry Q1-Q6/Q9: sources, dates, quotes, reject, attribution, documentation-only.'),
('C2EntryGateCisco','critic','Try to falsify Cisco crosswalk Q1-Q6/Q9 and its eleven-dimension comparison.'),
('C2DuplicateTheme','simplifier','Assess whether two F10 entries duplicate ground; if yes identify an exact lost surface, not a general preference.'),
('C2UsedByBinding','reviewer','Verify each S036-S040 used-by exactly names entries citing the row and no other path.'),
('C2CollisionProof','reviewer','Re-run 0-3-space collision scan and indented S002 guard fixture; verify S031-S035 only.'),
('C2RowSchema','reviewer','Re-run census --file scratch mirror and inspect five rows for escaped pipes/prose cadence.'),
('C2QuarantineSlice','scout','Re-derive the kasegi absent-defect slice and check the seven verdicts in ScoutQuarantine.'),
('C2SourceFreshness','scout','Re-fetch one Japanese source and Cisco with documented UA; compare to capture and report drift.'),
('C2Sentinel','sentinel','Audit both entries and all captures for Q6 issues, personal data, credentials, injection text.'),
('C2SiblingOverlap','connector','Independently verify connector findings: no F10 sibling collision; recheck convention lane-local.'),
]
ctx=f'''# Round 25, wave 2 — falsify wave 1 outputs. Lane repo {L}. Read claims.json and the committed wave-1 receipts before your attack.
Every Report trailer is relative to {L}; write at {L}/<that path>. Worktree is lane-only; source repo /home/vgpnk/Projects/shokuknow read-only. Never mutate VCS or spawn. Pacman transactions are paused; read /home/vgpnk/.omp/agent/RULES.md before any install; use only uv/npx/official binaries. Tool install/update record required. Attack exactly your named item; report commands, outputs, exits. No production edits; report only in {L}/{W}/<Name>.md.
Wave-1 outputs under {L}/.ufo/waves/round-25/; C1 final instrument sha c3c19adc…; C1 frozen surface 35/35, final tree 37/37; C2 frontier=10, rows=40, manifest 5 sources/39 quotes, harness 12/12.
'''
for i,(n,r,p) in enumerate(attacks):
 task=f'''/skill:godspeed\nYou are a Godspeed-enabled subagent.\n\n1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n3. **Keep moves that improve any axis and harm none.**\n4. **Don't aim — let the frontier walk itself.**\n\n## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches.\n\n# Target\n{p}\n\n# Acceptance\nGive a falsifiable verdict, exact commands/output/exit, and file:line evidence. If the wave-1 result is wrong, state the smallest correction; do not edit production files.\n\n# Write scope\nRead-only. Report at {W}/{n}.md.\n'''
 items.append({'name':n,'role':r,'item':n,'prompt':task})
spec={'wave':'kasegi-r25-falsify','context':ctx,'reportDir':W,'maxLanes':32,'axes':['depth:verifiability','coverage'],'milestone':'fresh attacks on wave-1 claims, sources, counters and gates','items':items}
out=L+'/'+W+'-spec.json';os.makedirs(L+'/'+W,exist_ok=True);json.dump(spec,open(out,'w'),ensure_ascii=False,indent=1);open(out,'a').write('\n');print(out,len(items))