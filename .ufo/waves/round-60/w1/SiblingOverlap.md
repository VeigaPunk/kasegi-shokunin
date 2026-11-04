SCOPE CLEAR — no sibling lane's PROVINCE claims F41's ground, and F41 re-counts none of the held grounds F39, F40, F04 and S017; the one declared-boundary omission found in the F41 entry is reported as text below with one recommendation.

# SiblingOverlap — F41 cross-lane and held-ground overlap (kasegi round 60, wave w1)

Leaf seat; the item's three steps only (sibling scan, held-corpus reads, scope decision). No clone, fixture, exporter, mutant or probe tree was created; no lane command was run. Nothing under L was written except this file. No tool was installed or upgraded, so there is no install record. Path convention: a command block carrying `# cwd: <abs>` was run from that absolute directory; blocks without one use absolute paths themselves.

## 1. Step 1 — the sibling PROVINCE scan: four lines, three files, exit 0

Command, exactly as run (absolute glob, no cwd dependency):

```
grep -n -i -E 'Big Sleep|Fuzzilli|agentic|LLM-based bug|fuzzing|coverage-guided' /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md
```

Printed `lines=4`, `files=3`, exit 0 (same command redirected, then `wc -l`). The same glob counted per term, exit 0:

```
for t in 'Big Sleep' 'Fuzzilli' 'agentic' 'LLM-based bug' 'fuzzing' 'coverage-guided'; do n=$(grep -i -c -- "$t" /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md 2>/dev/null | awk -F: '{s+=$2} END{print s+0}'); printf '%-16s %s\n' "$t" "$n"; done
Big Sleep        2
Fuzzilli         1
agentic          2
LLM-based bug    0
fuzzing          0
coverage-guided  0
```

The four `path:line` hits are:

```
/home/vgpnk/Projects/shokunin/kama-shokunin/PROVINCE.md:186
/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md:207
/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md:209
/home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md:145
```

## 2. Every hit, and why none of them claims F41's ground

1. `/home/vgpnk/Projects/shokunin/kama-shokunin/PROVINCE.md:186` — "the adjacent processes the staged round-13 amendment names (the agentic-api gateway, the Semantic Router) stay refused: a gateway and a route-selection product are dispatch-side surfaces (`corpus/knowledge/cross-lane-scope.md`), reported to the owning lane, not absorbed." **Not F41**: serving-plane dispatch, an "agentic-api" gateway; the sentence is itself a refusal to absorb cross-lane scope.
2. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md:145` — "The ground named in `corpus/README.md` §Frontier: agentic benchmark task-spec audits (Terminal-Bench 2.0 / Toolathlon / SWE-bench Pro primary specs — unopened leads)". **Not F41**: kengaku's frontier is benchmark *task-spec* audits; F41 is a first-party production and re-discovery comparison, and F41's rows and entry fence the benchmark reading explicitly (item 4).
3. `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md:207` — the lane's own r59 amendment admitting F40 (the Big Sleep tracker). Own lane, prior frontier, not a sibling.
4. `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md:209` — the lane's own r60 amendment admitting F41. This is the object under test, not a competing claim.

## 3. Same-term confirmation — the six-term scan is lexical, so a differently-worded claim needs a second look

Command, exit 0, seven lines total:

```
grep -n -i -E 'vulnerab|exploit|bug bounty|security research|browser security|\bV8\b' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md /home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md /home/vgpnk/Projects/shokunin/kotoba-shokunin/PROVINCE.md /home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md
```

Distribution, counting the file column of the same output (`| cut -d: -f1 | sort | uniq -c`): kaidoku 3, kake 2, kotoba 1, revenger 1. Reading:

- kaidoku `:135`, `:138`, `:139` — consumer-side `.jsc` V8 bytecode and JS-source recovery, CDP runtime observation; no vulnerability discovery and no pipeline comparison.
- kake `:211` — a `security.txt` pointer to a reporting channel; kake `:290-292` — "Vulnerability handling itself stays out of province: report intake, triage, remediation, disclosure timing, bounty and policy operation ... are not kake's". Routes away.
- kotoba `:67` — "kasegi owns bounty and security research (programs, rules, claim packages ...)"; it assigns the ground, it does not claim it.
- revenger `:12-14` — "live-target activity, exploitation, third-party testing and disclosure outside the program channel remain outside this province." Refuses.

No sibling PROVINCE claims production vulnerability-discovery pipelines, V8 fuzzing, or an agent-versus-fuzzer comparison.

## 4. The lane's own boundary declarations the scan is measured against

- `PROVINCE.md:24-25` — **Owns** the domain; "**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it."
- `PROVINCE.md:47` chousa = research method and source hierarchy; `PROVINCE.md:50` kengaku = "LLM evaluation and benchmarks".
- `PROVINCE.md:209` scope limit: "the Big Sleep tracker stays F40, the Naptime research principles stay S010's ground, the AISI progress-rate measurement stays F39, cost-per-bug is explicitly not compared (S093.txt:41), the reverse experiment is not run (S093.txt:53), and no individual finding or issue is enumerated."
- `corpus/README.md:1005` F41 row; `corpus/SOURCES.md:100` S093 row — "not a general fuzzer-versus-agent benchmark, not the Big Sleep tracker (S092) and not the Naptime research principles (S010)".
- `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:14` — "not a benchmark of fuzzing against agentic analysis in general"; `:16` — "the entry does not read the post as a general fuzzer-versus-agent benchmark"; `:34` — "not vendor policy, a bounty-program rule, an intake channel or a severity ladder".

## 5. Held ground F39 — distinct: a progress-rate measurement, not a production-pipeline count

- `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:5` — `ground: F39`; `:18` and `:22` the measured object is the 80%-reliability cyber time horizon, "had doubled every 4.7 months since reasoning models emerged in late 2024", bounded by a 2.5M-token cap and a 4.1-to-5.0-month single-omission band.
- F41 measures a different object: hotlist report counts and a re-discovery share. Receipts from the capture:

```
# cwd: /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -n -i AISI corpus/source-snapshots/round-60/S093.txt    # → no output, exit 1 (0 hits)
$ grep -n -E '20 of 81|~?25%|70%|62%|45 vs|441|316' corpus/source-snapshots/round-60/S093.txt | cut -c1-300
16: ... BigSleep found more vulnerabilities ...
30:Fuzzilli: 316
31:BigSleep: 441
40:So in terms of vulnerabilities, it's roughly a tie (small advantage BigSleep) at the moment: 45 vs. 37.
51: ... an overlap of roughly 25% (20 out of a total of 81) ...
68: ... re-discover ~62% ... another ~12% ... around 26% ...
84:So the share of "correct" bugs found climbs to ~70% ...
$ grep -n -E '^(Fuzzilli|BigSleep): (178|95)$|1150|roughly 600|132 historic|112 bugs|25 attempts' corpus/source-snapshots/round-60/S093.txt | cut -c1-220
33:Fuzzilli: 178
34:BigSleep: 95
55: ... around 1150 raw bugs.
56: ... roughly 600 vulnerabilities.
60:We end up with 132 historic bugs.
61: ... a final number of 112 bugs.
65:We now run the agent for 25 attempts on each commit. ...
```

- No statistic is shared with F39: F39's figures are months, token caps and range attempt counts; F41's are the capture figures above. `AISI` occurs 0 times in the F41 source, so F39's ground is not re-counted.
- Same kind of subject, different object: F39's own entry carries the kengaku adjacency note at `:79-81`; the F41 entry carries none (item 9). That is a declaration difference, not a content overlap.
- `PROVINCE.md:209` already names F39 as held.

## 6. Held ground F40 — distinct: a different tracking surface for the same program

- F40 holds the Google Issue Tracker README: `corpus/knowledge/google-big-sleep-findings-tracker.md:3` source `https://issuetracker.google.com/issues/430375499`; `:24` the lead resolves to `https://issuetracker.google.com/savedsearches/7155917`; `:71` the saved search serves an SPA shell; `:72` states the saved search's result set is not enumerated in that entry.
- F41 counts a different system: `project-zero-fuzzilli-vs-bigsleep-comparison.md:20` "two Chromium hotlist queries"; the capture says "query issues from Chromium's bugtracker (where V8 bugs are tracked)" (`S093.txt:26`) with `hotlistid:5433121` (Fuzzilli) and `hotlistid:8067258` (BigSleep) at `S093.txt:27-28`, and Clusterfuzz-level duplicate handling at `S093.txt:48`.
- Cross-surface receipts:

```
# cwd: /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -c -E 'hotlist|Chromium|441|316|45 vs|re-discovery' corpus/knowledge/google-big-sleep-findings-tracker.md
0            # exit 1, no match
$ grep -c -i -- issuetracker corpus/source-snapshots/round-60/S093.txt
0            # exit 1, no match
```

- F41 entry `:42` — "enumerates no individual finding, no crbug.com reference and no tracker issue".
- Second-order effect to record: both entries describe Big Sleep on different populations — all disclosed findings collected in the tracker README versus V8-only Chromium hotlist entries in April-September 2026 (`S093.txt:26`). Their numbers must not be summed or used as a cross-check of one another; F41's "roughly 25% (20 out of a total of 81)" (`S093.txt:51`) is Fuzzilli-versus-BigSleep overlap inside the Chromium hotlist, not an overlap with F40's tracker.
- `PROVINCE.md:209` already names F40 as held.

## 7. Held ground F04 — distinct: a per-finding validation policy, not an aggregate measurement

- `corpus/knowledge/ai-assisted-finding-validation.md:6` — "Treat an AI-originated finding as a candidate, not a confirmed vulnerability, until its evidence package records a reproducible observation and human validation of the claimed impact and reachability."
- F41 states the complementary limit: `project-zero-fuzzilli-vs-bigsleep-comparison.md:38` — "no independent replication and no verification of any individual finding are asserted here".
- F41's entry mentions F04 zero times (item 9 command). No count and no rule are shared: F41's 45-vs-37 counts actionable Type-Vuln *reports*, and its Claim 2 falsifiable rule at `:22` already says the raw counts "are not vulnerability counts". Distinct by kind (aggregate throughput versus per-finding validation).
- Boundary caveat for the lead: F04 supplies the candidate/confirmed vocabulary that a reader of F41's 45-vs-37 needs, and F41 does not restate it (item 9).

## 8. Held ground S017 — distinct: a disclosure-timeline policy

- `corpus/knowledge/pz-reporting-transparency-trial.md:5` — `ground: F02` (a fourth disclosure-timeline shape); `:18` Big Sleep appears only as the trial's second participant ("will also be trialling this policy", S017.txt:L28).
- F41 has no timeline content: `grep -c -i -E '90-day|90\+30|notice milestone|reporting transparency'` on the F41 entry prints 0, exit 1. Per-term split on the S017 entry:

```
# cwd: /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ for t in hotlist Chromium Fuzzilli 'big sleep' bigsleep '\bV8\b'; do printf '%-10s %s\n' "$t" "$(grep -c -i -E -- "$t" corpus/knowledge/pz-reporting-transparency-trial.md)"; done
hotlist    0
Chromium   0
Fuzzilli   0
big sleep  7
bigsleep   0
\bV8\b     0
```

The seven `big sleep` hits are participation mentions, not production data. Distinct by kind (policy timing versus production counts).
- Note: S017 is held by F02; F40 only cites it. F41's `PROVINCE.md:209` scope limit names F40, S010 and F39 but not S017 (item 9).

## 9. The one gap found — a declaration omission inside the F41 entry, not a ground overlap

Command (F41 entry), exit 0:

```
# cwd: /home/vgpnk/Projects/shokunin/kasegi-shokunin
for t in kengaku S091 S092 S011 S012 S017 S009 S010; do printf '%-9s %s\n' "$t" "$(grep -c -- "$t" corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md)"; done
kengaku   0
S091      0
S092      0
S011      0
S012      0
S017      0
S009      0
S010      0
```

A broader token grep over the same entry, exit 0, returns one line (the word "tracker" inside a Limits bullet):

```
# cwd: /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -n -E 'F39|F40|F04|S017|S092|S010|S009|AISI|tracker|validat|candidate|disclos' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md | cut -c1-260
42:- The entry enumerates no individual finding, no crbug.com reference and no tracker issue; the post's figures (images) are not transcribed, and no claim rests on them.
```

So the F41 entry names no held-ground ID and no kengaku adjacency, while its siblings do: F40's Limits at `:79-81` names both S017 and F04, and F39's Limits at `:79-81` names kengaku.

The F41 entry fences by *kind* ("not a benchmark ... in general" at `:14`/`:16`; "not vendor policy, a bounty-program rule..." at `:34`) but not by *owner*. Under `PROTOCOL.md:457-459` — "Contested scope — evidence or work is reported in the lane report; the integrator arbitrates by refining `PROVINCE.md`" — this is not a contested scope: nothing is being absorbed or double-owned. It is an incomplete boundary statement inside one entry, reportable as text (recommendation below). The `## Limits` list is six bullets, lines 38-43 (`sed -n '38,43p' ... | grep -c '^- '` prints 6).

## 10. Step 3 — decision

Test applied: does any sibling lane's PROVINCE claim F41's ground, and does F41 re-count F39/F40/F04/S017?

- Items 1-3: no sibling claim. The two sibling hits are different objects (kama's serving plane, kengaku's benchmark task specs), and the security-term confirmation shows kake and revenger refusing the ground and kotoba assigning it to kasegi.
- Items 5-8: all four held grounds are distinct in object, numbers and kind; F39 and F40 are already fenced in `PROVINCE.md:209`, F04 and S017 are distinct but not named in that fence or in the entry.
- Residual: the entry-level naming omission in item 9. No claim value, ledger figure, counter or gate depends on it.

**Verdict: SCOPE CLEAR.** No contested-scope item is routed to the integrator. The omission is reported below as a text correction only.

## 11. Scratch and tooling

- Scratch `/fast/scratch/hyaku/kasegi-r60/SiblingOverlap` was created for three intermediate files (`hits.txt`, `termcounts.txt`, `security-hits.txt`) and removed with `rm -rf` before this file was written; the removal was checked with `test ! -e` (exit 0). No leftover is named.
- No tool was installed or upgraded; no credential material was read or written; the lane suite was not run; no git or jj mutation was made against L.

## Recommendation (one, text only — not applied)

Append one dated bullet to the F41 entry's `## Limits` list (lines 38-43), mirroring the convention already used by F40:79-81 and F39:79-81:

> - Held-ground and adjacency (added, non-claim boundary note): the AI-assisted-finding-validation method stays F04 (S009-S012) and the Project Zero 2025 trial text stays S017 (F02); the AISI progress-rate measurement stays F39 and the Big Sleep tracker stays F40, as the round-60 amendment records; LLM evaluation and benchmark method is kengaku's province (`PROVINCE.md`, Adjacent), and the re-discovery experiment's method is not re-scored here.

- Affected axes: **depth:verifiability** (the boundary becomes a checkable sentence, the same shape as F39 and F40) and **coverage** (the held-ground map is complete for this entry); neither frozen claim value moves.
- Risks: an appended bullet could be misread as a new claim or as a re-verification. Mitigation: mark it dated and non-claim, and leave the `source:` and `verified-at:` lines untouched. It does not touch the S093 capture digest, the knowledge file count, `knowledge-expected.txt`, or any C1 instrument value.
- Verification after appending: `grep -c -E 'F04|S017|F39|F40|kengaku'` on the entry is nonzero per token; `grep -c 'FIG '` on the entry stays 0; C2's counting commands 4-6 are unchanged because no file is added, renamed or re-sourced.
