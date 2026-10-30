# R48Probe32 — bounded grammar probe: SHONEN box 3 duplicate

Seat: R48Probe32 (leaf member, no subagent dispatch). Lane root: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Frozen claim: .ufo/waves/round-48/claims.json (sha256 b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345).

## Inputs read
- /home/vgpnk/.omp/agent/RULES.md (read first; tooling directive — no tool installs performed in this seat).
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/controls/protocol-source.txt (read, lines 1-300 of 544). Relevant content: a shonen→shokunin promotion requires every SHONEN.md box checked by a non-author verifier; `[~]` is author assertion; `[x]` needs a named non-author verifier.
- Frozen counter: /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py (sha256 0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd). Read-only; not edited.
- Canonical fixture: /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md (sha256 b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0, 12 lines, 761 bytes). Not edited; re-hashed after the probe, unchanged.
- Round-47 routes R1/R2: the round-47 verifier spotcheck cites `corpus/QUALITY.md:35` as R1 (as-of discipline for dated source behaviour; see `.ufo/waves/round-47/w1/R47RevScopeout.md:17`). R1 concerns source time-scope, not checklist grammar, so this probe does not exercise it. I did not locate a distinct R2 route text in the files read and make no claim about R2.

## Counter grammar (as read)
`grade()` requires, in order: a trailing `\n` and no `\r`; the three-line preamble after the heading; then for each of the four fixed LABELS, in order, exactly one line matching `- [ ~x] <label>` (re.fullmatch), optionally followed by one `      Evidence: <one repo-relative pointer>[ — text]` line. Mark `x` yields `SF-VERIFIER`; a non-space mark without evidence yields `SF-EVIDENCE`; a box line that does not fullmatch the expected next LABEL yields `SF-BOX`; any leftover line yields `SF-TRAILING`; success yields `SF-CLEAN`.

## Probe (box 3 only)
Scratch: /fast/scratch/hyaku/kasegi-r48/R48Probe32/ (created explicitly).
- pristine-SHONEN.md: byte copy of canonical SHONEN.md (sha256 b1352168…a46d0, confirmed equal).
- mutated-box3-dup-SHONEN.md: pristine with lines 9–10 (box 3 line `- [~] Instructions executable by an agent without oral context` and its `      Evidence:` line) duplicated byte-exact immediately after line 10. Boxes 1, 2, 4 and the preamble are byte-unchanged. Resulting sha256 4006c539644e9a2d3a25388282f07f060daf4a17175c7654dbfbf7302dbb983d, 14 lines.
- restored-SHONEN.md: byte copy of pristine, re-verified with cmp.

## Commands and observed output
```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe32/pristine-SHONEN.md
shonen-form canonical=1 finding=SF-CLEAN exit=0          # run 1, exit 0
shonen-form canonical=1 finding=SF-CLEAN exit=0          # run 2, exit 0
$ python3 .../shonen-form.py --root .../kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe32/mutated-box3-dup-SHONEN.md
shonen-form canonical=0 finding=SF-BOX exit=1            # run 1, exit 1
shonen-form canonical=0 finding=SF-BOX exit=1            # run 2, exit 1
$ python3 .../shonen-form.py --root .../kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe32/restored-SHONEN.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
```
Byte-level receipts: `sha256sum` before b1352168…a46d0, mutant 4006c539…983d, restored b1352168…a46d0; `cmp pristine restored` identical. Production SHONEN.md after the probe: b1352168…a46d0 (unchanged).

## Expected vs observed
- Pristine positive control: expected clean, exit 0, SF-CLEAN, stable across runs. Observed: `SF-CLEAN exit=0` twice. MATCH.
- Box-3 duplicate: expected non-clean, stable finding. Observed: `SF-BOX exit=1`, stable across two runs. MATCH.

## Mechanism of the SF-BOX finding
After box 3 and its evidence line are consumed, the counter advances to the next expected LABEL (box 4, "No cross-domain bleed …"). The line at that position is the duplicated `- [~] Instructions executable …` line, which does not fullmatch box 4's label, so `grade()` returns `SF-BOX` at that position. The finding is thus the counter's ordinary rejection of a fifth box-shaped line inside a four-box fixed sequence.

## Semantic permissibility of the transformation
The duplicate is not semantically permitted by the canonical form. The canonical form is "all of" four named boxes in a fixed order, with no provision for repeated or extra boxes. A duplicated box-3 line is a fifth checklist item that the protocol does not define, so the non-clean verdict is correct. No counter defect is claimed, and no defect is fabricated.

## Limits and non-claims
- Author-side form check only. SF-CLEAN here is not promotion and not semantic truth; `[~]` lines remain author assertions under the protocol gate.
- No production file was edited; the frozen counter bytes were not altered; no fix was applied to any finding.
- The round-level milestone (one frozen canonical-form repair plus 64 distinct probes) is a wave-level target. This seat delivers one probe as assigned and proposes no repair.
- No tool installs or upgrades were performed by this seat. Python 3.14.8 was the pre-existing interpreter.
- No subagent dispatch, no background jobs, no git/jj operation, no commits.

## Cleanup
Scratch /fast/scratch/hyaku/kasegi-r48/R48Probe32/ (pristine, mutant, restored copies) removed on exit after the receipts above were captured here. Only this report was written in the lane.
