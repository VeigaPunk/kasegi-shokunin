VERDICT: SCOPE CLEAR for F39 — IN SCOPE for kasegi, with the sibling-owned method ground (kengaku's METR-style time-horizon measure) reported, not absorbed. Sibling-overlap counts: 0 word-boundary hits for the 9 target tokens across the 20 sibling PROVINCE.md files (the only 2 case-sensitive hit lines are the lane's own F39 line and a false positive); 1 sibling lane (kengaku) holds real adjacent ground (METR time horizon, S013/S014); 0 sibling files contain 'aisi.gov.uk' or 'AI Security Institute'. Lane-corpus scan: 32 raw hit lines over 9 tokens in 77 knowledge files — 25 in the F39 entry itself, 6 substring false positives ('METR' inside 'TELEMETRY_EVENTS'), 1 passing mention (Mythos in Anthropic's own program). One in-lane adjacency not recorded by the F39 entry: the round-24 Anthropic capture already carried an AISI cyber-range claim (corpus/source-snapshots/round-24/S012.txt:32) — the lane's own r52 annotation pattern (PROVINCE.md:194) would cover it; reported as text only.

Seat: SiblingOverlap (Kasegi lane, round 58, wave 1). Scope: adjacency and sibling-overlap scan for frontier entry F39 (UK AI Security Institute autonomous cyber-capability progress rate, source S091).
Lane under test: /home/vgpnk/Projects/shokunin/kasegi-shokunin, WORKING TREE at implementation commit 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b; freeze commit for the frozen claims 543cac13886b91ac660d788ed20e64ae70ee0fa5.
Read-only on L. Nothing written to L except this file. No git mutation of any kind against L (only `git -C L show/rev-parse/log/status`, all read-only).
Sibling PROVINCE.md files read: /home/vgpnk/Projects/shokunin/{audio,chousa,game-dev-2d,game-dev-3d,kagi,kaidoku,kake,kama,kengaku,kotoba,kotodama,kumitate,lore,mado,mori,revenger,souji,tabi,tameshi,tsukuroi}-shokunin/PROVINCE.md — 20 siblings, plus kasegi's own PROVINCE.md.
Scratch: /fast/scratch/hyaku/kasegi-r58/SiblingOverlap (e1.txt, e1b.txt, final-evidence.txt) — deleted before yield; no leftovers.
Tools: none installed or upgraded (the operator directive of 2026-10-19 was read at /home/vgpnk/.omp/agent/RULES.md; no package was needed for a read-only grep/analysis seat, and pacman was not touched).
No credential material was written to any file: no secrets, tokens, cookies, session values or op:// references appear here.

## 1. What F39 claims, and the two sentences that decide its scope

$ sed -n '205p' /home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md | cut -c1-200
[r58 Frontier amendment, appended 2026-11-03, end-of-file append per R6] F39 — UK AI Security Institute autonomous cyber-capability progress rate (the institute's own dated, suite-bound measurement statements: the 80%-reliability cyber time-horizon doubling estimate and its acceleration, the bounded method and its stated uncertainty, and the cyber-range results) — admitted round 58; entry corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md (source S091; capture corpus/source-snapshots/round-58/S091.txt); scope limit: the statements of one government institute about its own closed testing only — LLM evaluation method stays adjacent to kengaku (Adjacent above), the underlying runs are unpublished, and MET…
[exit=0]

The scope-limit clause, quoted in full:

$ python3 -c "d=open('PROVINCE.md').read().split('\n'); l=d[204]; i=l.find('scope limit'); print(repr(l[i:]))"
"scope limit: the statements of one government institute about its own closed testing only — LLM evaluation method stays adjacent to kengaku (Adjacent above), the underlying runs are unpublished, and METR's software-engineering doubling and the Frontier AI Trends Report stay unabsorbed"

The lane's own Adjacent section (the "Adjacent above" the clause points to):

$ sed -n '43,52p' PROVINCE.md
## Adjacent
(blank)
Sibling lanes are reported, not absorbed:
(blank)
- chousa — research method and source hierarchy
- kagi — secrets and vault handling
- kake — web properties
- kengaku — LLM evaluation and benchmarks
(blank)
Live-target testing is refused; this corpus is documentation only.

Deciding sentence inside the F39 entry itself (the (a)-overlap ground, reported not absorbed):

$ sed -n '81,84p' corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md
- Adjacency: LLM evaluation and benchmark method is kengaku's province (PROVINCE.md, Adjacent). This
  entry records one government institute's cyber-task measurement statements because they bear on
  vulnerability-finding throughput planning; the method itself is not re-scored here.

Deciding sentence in the sibling that owns the overlapping surface (NOT in kengaku's PROVINCE.md — see §7):

$ sed -n '59p' /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md
| `knowledge/agent-time-horizon-and-task-validity.md` | METR human-duration time horizon (task difficulty at a stated success probability, not wall-clock or job automation) + coding-benchmark task/test validity audits | S013, S014 — `corpus/SOURCES.md` rows, round 24 |

$ grep -n '^| S013 \|^| S014 ' /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md | cut -c1-150
35:| S013 | Measuring AI Ability to Complete Long Software Tasks — https://arxiv.org/html/2503.14499 | paper | A | its own time-horizon measure and ...
36:| S014 | Task-Completion Time Horizons of Frontier AI Models — https://metr.org/time-horizons/ | dataset | A | METR's own measure definition and ...

## 2. Sibling PROVINCE.md scan — the 9 target tokens

21 PROVINCE.md files exist under /home/vgpnk/Projects/shokunin/*-shokunin/ (20 siblings + kasegi's own). The lane's Adjacent section names four of them (chousa, kagi, kake, kengaku); all 20 siblings were scanned.

$ ls -d */PROVINCE.md | wc -l ; ls -d */PROVINCE.md | grep -vc '^kasegi-shokunin/'
21
20

### 2.1 Case-sensitive raw-substring scan (the token list exactly as specified)

$ grep -nE 'AI Security Institute|AISI|time horizon|time-horizon|METR|Mythos|GPT-5\.5|cyber range|autonomous cyber' */PROVINCE.md | cut -d: -f1,2
kasegi-shokunin/PROVINCE.md:205
mado-shokunin/PROVINCE.md:32
[exit=0]

Two hit lines only. Classification:

| file:line | token matched | what it actually is | classification |
|---|---|---|---|
| kasegi-shokunin/PROVINCE.md:205 | 'AI Security Institute' (col 83), 'autonomous cyber' (col 105), 'time-horizon' (col 237), 'AISI' (col 410, inside the entry filename `aisi-autonomous-cyber-capability-progress-rate.md`), 'METR' (col 725) | the lane's own F39 amendment line | **the subject under test** — the lane's own province surface, not a sibling |
| mado-shokunin/PROVINCE.md:32 | 'METR' (col 544) | substring of the identifier `MADO_GEOMETRY:` | **false positive** — no METR reference |

### 2.2 Case-insensitive, word-boundary scan over the 20 siblings (kasegi excluded)

$ grep -niE '\bAI Security Institute\b|\bAISI\b|\btime[ -]horizons?\b|\bMETR\b|\bMythos\b|\bGPT-?5\.5\b|\bcyber ranges?\b|\bautonomous cyber\b' */PROVINCE.md | grep -v '^kasegi-shokunin/'
(no output)
[exit=1 — no match]

Zero sibling PROVINCE.md hits. The only word-boundary hit anywhere in the 21 files is kasegi's own line 205:

$ grep -niE '\bAI Security Institute\b|\bAISI\b|\btime[ -]horizons?\b|\bMETR\b|\bMythos\b|\bGPT-?5\.5\b|\bcyber ranges?\b|\bautonomous cyber\b' */PROVINCE.md | cut -d: -f1,2
kasegi-shokunin/PROVINCE.md:205

### 2.3 The 41 case-insensitive raw-substring hits, all classified

$ python3 - <<'PY' (over each */PROVINCE.md, re 'aisi|METR', case-insensitive, printing the host word)
41 raw hits. 1 is the lane's own F39 line (2 tokens: 'aisi' in the entry path, 'METR' proper). The other 40 are substrings of unrelated words:

| host word | tokens | count | files |
|---|---|---|---|
| `metrics` / `metric` | 'metr' | 14 | audio:26, audio:31, kasegi:114, kasegi:195, kengaku:742, mado:175, mado:176, tameshi:103, plus 'Metr' in mado:162/168×2/180×2, kasegi:114 |
| `telemetry` | 'metr' | 16 | kengaku:3, :8, :13, :16×2, :17×2, :51, :53, :76, :79, :81, :142, :159, :160, :161; mori:57×2, :118 |
| `geometry` / `GEOMETRY` / `geometric` | 'metr' | 8 | game-dev-2d:27, game-dev-3d:66, mado:32×2 |
| `ASYMMETRY` | 'metr' | 1 | tabi:37 (via kaidoku's queue file, see §3) |
| `cap-raising` | 'aisi' | 1 | kaidoku:86 — "no cap-raising knob ex…" contains the letters a-i-s-i inside "raising" |

$ python3 -c "l='  organic cores still exceed the cap; no cap-raising knob exists. Retention decays oldest-first.'; print(l.find('aisi'))"
46

Proof that the kaidoku hit is 'aisi' inside "raising", not the institute: the matched substring is at index 46 of that line and reads `aisi` inside `cap-raising`.

### 2.4 Conclusion of the PROVINCE scan

No sibling PROVINCE.md names AI Security Institute, AISI, a time horizon, METR, Mythos, GPT-5.5, a cyber range, or autonomous cyber capability. The nearest sibling *surface* (kengaku's METR time horizon) is declared in kengaku's corpus, not in kengaku's province text — quantified in §7.

## 3. Sibling corpora scan — where the real adjacent ground sits

### 3.1 Sibling corpus/knowledge file lists for the 9 tokens

$ for d in <20 siblings>; do for p in <9 tokens>; do grep -rIl -e "$p" "$d-shokunin/corpus/knowledge"; done; done
kaidoku        pat=METR                     2026-10-14-r9-01-queue-a-ops.md
kama           pat=METR                     consumer-registry.md
kengaku        pat=time horizon             agent-time-horizon-and-task-validity.md
kengaku        pat=time-horizon             agent-time-horizon-and-task-validity.md benchmark-task-validity-checklist.md
kengaku        pat=METR                     agent-time-horizon-and-task-validity.md bench-arena-fresh-run.md
kotoba         pat=METR                     sibling-citation-routing-round16.json
kotodama       pat=time horizon             civilizations/africa-primary-sources.md
kumitate       pat=METR                     kimi-session-state.md live-surface-probe.md reconcile-and-cycle.md
mado           pat=METR                     hyprland-gkeep-geometry-r43.md
tabi           pat=METR                     webview2-control-keys-round-55.md
(no other sibling produced any list)

Per-hit classification of the host word:

$ grep -o -n -E '.{0,12}METR.{0,12}' <each file> | head -3
kaidoku …231:  ASYMMETRY vs the ledger ve…          → false positive
kama   …110:oop.sh:5` (`METRICS_URL=${LL…            → false positive (METRICS_URL)
kengaku bench-arena-fresh-run.md …19,94: `LLAMA_METRICS_URL` / `METRICS_URL` → false positive
kotoba …1062:DURABLE_TELEMETRY_KINDS",             → false positive
kumitate … `TELEMETRY_SCOPE` / `DURABLE_TELEMETRY_KINDS` (×3 files) → false positive
mado   … `GEOMETRIC_GOAL` / `GetSystemMetrics` / `WindowMetrics` → false positive
tabi   …37:CLOSED ASYMMETRY:                        → false positive

Two real hits:

| file:line | token | what it is | classification |
|---|---|---|---|
| kengaku-shokunin/corpus/knowledge/agent-time-horizon-and-task-validity.md:1,5,9,16,23,29,33,39,40,46 | 'METR', 'time horizon' | kengaku's admitted **METR-style time-horizon measure** (S013/S014): "A METR-style time horizon is the human completion duration associated with a stated predicted success probability on a specified task suite" | **sibling-owned surface that F39 abuts** — classification (a), reported not absorbed. The entry's :81-84 Limits bullet declines to re-score the method, and the F39 scope limit excludes METR's doubling figure from absorption (entry :76-78) |
| kengaku-shokunin/corpus/knowledge/benchmark-task-validity-checklist.md:19 | 'time-horizon' | cross-reference: "This entry extends `knowledge/agent-time-horizon-and-task-validity.md`" | **passing mention** — same sibling surface, referenced not re-asserted |
| kotodama-shokunin/corpus/knowledge/civilizations/africa-primary-sources.md:134 | 'time horizon' | "Define one claim and its scale: a person, institution, town, language variety, or time horizon—not 'Africa.'" | **false positive for F39** — historical/geographic scale sense, unrelated to the metric |

### 3.2 Whole sibling trees (corpus + PROVINCE.md + SKILL.md) for the F39 surface itself

$ for d in <20 siblings>; do grep -rIl -i 'AI Security Institute' "$d-shokunin/corpus" "$d-shokunin/PROVINCE.md" "$d-shokunin/SKILL.md"; done
(no output — 0 files in all 20 siblings)
[exit=0]

$ for d in <20 siblings>; do grep -rIl 'aisi.gov.uk' "$d-shokunin/corpus" "$d-shokunin/PROVINCE.md" "$d-shokunin/SKILL.md"; done
(no output — 0 files in all 20 siblings)

$ for d in <20 siblings>; do for p in 'cyber range' 'autonomous cyber' 'capability progress'; do grep -rIl -i "$p" "$d-shokunin/corpus" "$d-shokunin/PROVINCE.md"; done; done
(no output — 0 files in all 20 siblings)

The AISI cyber-capability-progress-rate surface is held by **no** sibling lane. F39 does not collide with any sibling's held ground.

### 3.3 One AISI artefact DOES sit in a sibling corpus — and it is a different AISI surface

$ for d in <20 siblings>; do grep -rIl 'UK AISI' "$d-shokunin/corpus" "$d-shokunin/PROVINCE.md" "$d-shokunin/SKILL.md"; done
kengaku      kengaku-shokunin/corpus/evidence/round53/fetched/C1PriceL1-general-best-practices.html kengaku-shokunin/corpus/evidence/round53/fetched/C1PriceScoutD-row-gcode-to-text__arxiv-2507.02825v1.html

$ grep -n 'UK AISI' /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round53/fetched/C1PriceL1-general-best-practices.html | cut -d: -f1
297
302
307
312

$ python3 -c "import re; d=open('.../C1PriceL1-general-best-practices.html').read(); print(re.search(r'<title>(.*?)</title>',d,re.S).group(1)); print(re.findall(r'ltx_role_affiliation\".*?ltx_text\">([^<]{2,60})</span>',d,re.S)[:12])"
Establishing Best Practices for Building Rigorous Agentic Benchmarks
['UIUC', 'UIUC', 'Stanford University', 'University of California, Berkeley', 'Yale University', 'Princeton University', 'MIT', 'Transluce', 'ML Commons', 'ML Commons', 'Amazon', 'Amazon']

$ python3 -c "...; [print('UK-AISI author:', m.group(1).strip()) for m in re.finditer(r'ltx_personname\">\s*([^<]{2,60})', d) if 'UK AISI' in d[m.end():m.end()+900]]"
UK-AISI author: Jwala Dhamala
UK-AISI author: Jacob Merizian
UK-AISI author: Mario Giulianelli
UK-AISI author: Harry Coppock
UK-AISI author: Cozmin Ududec

$ grep -n '2507.02825' /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md | cut -c1-200
104:| S091 | Agentic Benchmark Checklist (ABC) — https://arxiv.org/abs/2507.02825 | paper | A | the published checklist this lane's task-validity axes restate, re…

Classification: **sibling-owned surface, different subject.** kengaku holds an AISI-*authored* paper (the Agentic Benchmark Checklist) as its own registry row S091, and the fetched bytes carry five UK AISI affiliations. That is AISI's benchmark-methodology surface, not AISI's own cyber-capability measurement programme (the F39 subject). No F39 claim touches it. Two consequences worth recording:
  (i) the two lanes' registries both use the id **S091** for different documents (kasegi S091 = the AISI blog; kengaku S091 = the ABC checklist). Per-lane registries, so no rule is broken, but any cross-lane "S091" reference is ambiguous.
  (ii) forward-looking adjacency: if the lane ever opens AISI's *benchmark-method* work (not the blog), the boundary to kengaku's S091 / S077–S090 task-validity ground bites immediately.
Observation, not a correction (sibling-lane files are read-only here): the fetched bytes are stored twice under two names with identical sha256, one of which misdescribes its content — `C1PriceScoutD-row-gcode-to-text__arxiv-2507.02825v1.html` is the ABC paper (title "Establishing Best Practices for Building Rigorous Agentic Benchmarks", 0 occurrences of "gcode"). kasegi cannot and does not touch kengaku's corpus; reported to the orchestrator only.

## 4. Lane corpus scan (kasegi's own corpus — 77 knowledge files)

$ ls corpus/knowledge/*.md | wc -l
77

$ grep -nE 'AI Security Institute|AISI|time horizon|time-horizon|METR|Mythos|GPT-5\.5|cyber range|autonomous cyber' corpus/knowledge/*.md | wc -l
32

Per-pattern file lists:

$ for p in 'AI Security Institute' 'AISI' 'time horizon' 'time-horizon' 'METR' 'Mythos' 'GPT-5\.5' 'cyber range' 'autonomous cyber'; do grep -rIlc -e "$p" corpus/knowledge/*.md; done
AI Security Institute    aisi-autonomous-cyber-capability-progress-rate.md
AISI                     aisi-autonomous-cyber-capability-progress-rate.md
time horizon             aisi-autonomous-cyber-capability-progress-rate.md
time-horizon             aisi-autonomous-cyber-capability-progress-rate.md
METR                     aisi-autonomous-cyber-capability-progress-rate.md mission-ledger.md ops-invariants.md source-tree-loss-2026-09-28.md triage-thresholds.md
Mythos                   ai-assisted-finding-validation.md aisi-autonomous-cyber-capability-progress-rate.md
GPT-5\.5                 (no file)
cyber range              aisi-autonomous-cyber-capability-progress-rate.md
autonomous cyber         aisi-autonomous-cyber-capability-progress-rate.md

Every one of the 32 hit lines, classified:

| file:line | token | what it is | classification |
|---|---|---|---|
| aisi-autonomous-cyber-capability-progress-rate.md — 25 hit lines (:1, :3, :10, :12, :18, :22, :25, :26, :28, :32, :34, :42, :43, :45, :49, :51, :53, :56, :57, :60, :64, :65, :66, :67, :76) | all nine tokens | the F39 entry itself | **admitted entry** — lane-owned ground, the subject under test |
| ai-assisted-finding-validation.md:25 | 'Mythos' | S012, Anthropic's own open-source program: "…reproduce the issue that Mythos has found and re-assess its severity" | **passing mention** — Anthropic's bug-finding program (F04), a different surface from AISI's measurement programme; the F39 entry's Mythos mentions are the same model family but a different subject (a checkpoint measured by AISI) |
| mission-ledger.md:87 | 'METR' | substring of `TELEMETRY_EVENTS` | false positive |
| ops-invariants.md:22 | 'METR' | substring of `TELEMETRY_EVENTS` | false positive |
| source-tree-loss-2026-09-28.md:116, :277, :279 | 'METR' | substring of `TELEMETRY_EVENTS` | false positive |
| triage-thresholds.md:394 | 'METR' | substring of `TELEMETRY_EVENTS` | false positive |

Lane-side registry / README hits (same tokens, lane-owned surfaces):

$ python3 (scan of corpus/README.md and corpus/SOURCES.md for the 9 tokens)
corpus/README.md:953, :954, :955, :960, :964 — the round-58 admission block and the F39 row (admitted entry, lane-owned)
corpus/SOURCES.md:98 — the S091 registry row (admitted registry row)
corpus/SOURCES.md:142 — the AISI lead line (byte-unchanged; base :141, tip :142 — the same pointer drift the C2 reviewer logged as F1; the sha256 631364e0…627547 is unchanged)
corpus/SOURCES.md:215 — the round-58 registry-change bullet

Corpus-wide 'GPT-5.5' check (the token the specification listed but that no lane knowledge file carries):

$ grep -rIn 'GPT-5\.5' corpus/ | cut -c1-130
corpus/source-snapshots/round-24/S011.txt:853
corpus/source-snapshots/round-58/S091.txt:14, :16, :25, :26, :34
corpus/source-snapshots/round-58/S091.txt:43 ("GPT 5.5", space form)

The F39 entry records the Mythos Preview cyber-range results but not GPT-5.5's "GPT-5.5 solved 'The Last Ones' on 3 of 10 attempts" (S091.txt:34). This is a coverage matter for the C2/entry-claim-table seats, not an adjacency matter; recorded here only because the token was in the scan list, with the exact anchor so it is not lost.

## 5. THE adjacency finding: the lane already held an AISI cyber-range claim before F39

$ sed -n '32p' corpus/source-snapshots/round-24/S012.txt | cut -c1-400
The UK's AI Security Institute reports that Mythos Preview is the first model to solve both of their cyber ranges (simulations of multistep cyberattacks) end to end;

$ grep -n 'first model to solve' corpus/knowledge/*.md ; echo exit=$?
(no output) [exit=1 — no lane knowledge file quotes it]

$ grep -rn 'S012.txt:32' corpus/ .ufo/waves/round-58/ 2>/dev/null ; echo exit=$?
(no output) [exit=0]

Facts:
  - corpus/source-snapshots/round-24/S012.txt is the Anthropic "Project Glasswing: An initial update" post, dated May 22, 2026 (S012.txt:6-7 "Published"), captured in round 24 and already a held registry row (S012, Anthropic's own program report).
  - Its line 32 states AISI's cyber-range result in the second hand, one month before the F39 capture.
  - The F39 entry (S091.txt:34) says of the newer checkpoint: "This was the first time that a model completed the second of our two cyber ranges" (S091.txt:34), with the caveat "These results utilise a newer Mythos Preview checkpoint than that included in previous AISI reporting" (S091.txt:35).
  - So the two statements are consistent (the round-24 text reflects the earlier AISI reporting; the F39 text the newer checkpoint), but the lane's F39 entry records the AISI cyber-range surface as if new and does not note that a round-24 capture in the same lane already carried AISI's cyber-range claim.
  - The lane has its own precedent for recording exactly this class of observation: the r52 adjacency annotation, PROVINCE.md:194 — "[r52 adjacency annotation, appended 2026-11-01, factual, append-only — the round-51 closure's neighbor-screen observation] … one byte OUTSIDE that scope also named the surface at the round-51 base: corpus/source-snapshots/round-24/S013.txt:65 …". The F39 round has no such annotation for S012.txt:32.
  - A second, smaller in-lane cross-reference exists: corpus/source-snapshots/round-40/S025.txt:881-885 (the CVE-Bench capture the lane holds) already cites "AI Security Institute, U. Inspect AI: Framework for Large Language Model Evaluations", and S025.txt:1333 "CVE-Bench is fully integrated with inspect ai, an open-source framework for LLM evaluations (AI Security Institute)". So AISI's LLM-evaluation-framework surface (Inspect AI) is already visible inside the lane's own corpus, and it is the concrete reason the F39 scope limit routes "LLM evaluation method" outward rather than inward.

Classification of this finding: **(b) lane-owned ground the entry extends**, with a missing cross-reference. It is not a sibling overlap: the prior mention is inside kasegi's own corpus, and no sibling lane holds it.

## 6. Scope verdict for F39

Verdict: **IN SCOPE for kasegi**, with the sibling-owned overlap **reported, not absorbed**.

| # | F39 surface element | sibling owner | sibling sentence that owns it (quoted) | classification | lane treatment (verified) |
|---|---|---|---|---|---|
| 1 | the AISI cyber-capability-progress-rate measurement record itself (80%-reliability cyber time-horizon doubling 4.7 months, acceleration from the Nov 2025 8-month estimate, bounded method, 4.1–5.0 month band, cyber ranges 6-of-10 and 3-of-10) | **none** — 0 sibling files contain 'aisi.gov.uk' or 'AI Security Institute'; 0 sibling PROVINCE.md hits for any of the 9 tokens (§2.2, §3.2) | — | **(b) lane-owned ground the entry extends** | entry records AISI's first-party statements; `ground: F39` (entry :5); registry row S091 (corpus/SOURCES.md:98) |
| 2 | the *method* — 80%-reliability time horizon over an expert-time-baselined cyber task suite, curve-fit doubling rate | **kengaku** | kengaku corpus/README.md:59 "METR human-duration time horizon (task difficulty at a stated success probability, not wall-clock or job automation) + coding-benchmark task/test validity audits \| S013, S014 — `corpus/SOURCES.md` rows, round 24"; kengaku corpus/README.md:312 "**Agentic time horizon and task validity**: covered at source-digest depth (round 24) — knowledge/agent-time-horizon-and-task-validity.md; sources S013, S014, S005, S006." | **(a) overlap with a sibling-owned surface — report, do not absorb** | entry :81-84: "the method itself is not re-scored here"; entry :76-78: "METR's software-engineering doubling time of 4.2 months … is a different programme's figure, named by the report and not absorbed here"; PROVINCE.md:205 scope limit excludes it |
| 3 | METR's own figure (4.2 months software doubling, S091.txt:32 and footnote 3 at :44) | **kengaku** (S013/S014 hold METR's measure and data) | same two README sentences above | **(a) reported, not absorbed** | named in the entry's Limits bullet only; `grep '\bMETR\b' corpus/knowledge/` returns exactly one line (entry :76) — no METR figure is asserted anywhere in the lane's knowledge |
| 4 | the "Frontier AI Trends Report" linked from the AISI page (S091.txt:2) | no owner; not opened, not a row | — | **neither** — named-not-opened | entry :77-78 "is named and not opened: a lead, not a row"; see correction C2 in §8 |
| 5 | the AISI cyber-range claim (Anthropic's second-hand statement, round-24 S012.txt:32) | none — inside kasegi's own corpus | — | **(b) lane-owned ground already held; missing cross-reference** | not cross-referenced by the F39 entry and not registered as an adjacency annotation (lane precedent PROVINCE.md:194) — finding in §5 |
| 6 | AISI-as-benchmark-author (ABC checklist, arXiv 2507.02825) | **kengaku** (its S091) | kengaku corpus/SOURCES.md:104 "| S091 | Agentic Benchmark Checklist (ABC) — https://arxiv.org/abs/2507.02825 | paper | A | the published checklist this lane's task-validity axes restate, read at its own abstract |" | **(c) none for F39** — different AISI surface, not touched by F39 | no F39 claim references it |
| 7 | every other sibling-token hit (metrics / telemetry / geometry / ASYMMETRY / "cap-raising") | — | — | **(c) none — false positives** | — |

The sentence that decides the scope limit's accuracy: the F39 clause routes "LLM evaluation method" to kengaku via kasegi's own Adjacent list (PROVINCE.md:50 "- kengaku — LLM evaluation and benchmarks"), and kengaku's own province text supports that routing — kengaku PROVINCE.md:3 "**Domain:** LLM/model research & evaluation — scopes ~/Projects/webzites/repos/llm-wiki, route telemetry" and kengaku PROVINCE.md:124-128 "The ground named in `corpus/README.md` §Frontier: agentic benchmark task-spec audits (Terminal-Bench 2.0 / Toolnasium / SWE-bench Pro primary specs — unopened leads), contamination transparency cards, judge calibration applied to this lane's own grader/attribution outputs, an identity-verified endpoint for novelty probes, and non-karpathy wiki topics (source absent)." The routing is therefore correct; see C1 in §8 for the one precision gap in the pointer.

## 7. Is the scope limit accurate against kengaku's PROVINCE text? (specification item 4)

$ for p in '\bMETR\b' 'time[ -]horizon' 'agent-time-horizon' 'UK AISI'; do printf '%-22s ' "$p"; grep -cE "$p" /home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md; done
\bMETR\b               0
time[ -]horizon        0
agent-time-horizon     0
UK AISI                0

Result: **the scope limit's *substance* is accurate; its *pointer* is imprecise.**

Accurate: kasegi's PROVINCE.md:205 says "LLM evaluation method stays adjacent to kengaku (Adjacent above)", and kasegi's Adjacent section does name kengaku for exactly that (PROVINCE.md:50 "- kengaku — LLM evaluation and benchmarks"). kengaku's own province text declares the domain "LLM/model research & evaluation" (kengaku PROVINCE.md:3) and its Frontier paragraph names the benchmark-method surfaces it holds (kengaku PROVINCE.md:124-128, quoted in §6). Nothing in F39 re-scores that method: entry :81-84 and the F39 scope limit both withhold it, and METR's own figure is named-not-absorbed (entry :76-78). The lane's refusal clause is therefore substantively correct.

Imprecise: the specific sibling-owned surface F39 abuts is the METR-style time-horizon measure, and kengaku's PROVINCE.md does not name it anywhere (four greps, all 0). Its owning sentences live in kengaku's *corpus* — corpus/README.md:59 and :312, and registry rows S013/S014 at corpus/SOURCES.md:35-36. A reader who follows "Adjacent above" into kengaku's PROVINCE.md cannot verify from that file that the time-horizon measure is kengaku's; the verification requires kengaku's corpus. This is the only inaccuracy found in the scope-limit text, and it is a pointer-precision issue, not a boundary error.

Two further accuracy checks on the same clause, both passing:
  - "the underlying runs are unpublished" — the entry says so at :14-15 ("it does not verify any model behaviour and does not verify the underlying runs, which the report does not publish"), and the capture contains no run data beyond AISI's own summary (S091.txt:23, :25, :28, :30, :34).
  - "the statements of one government institute about its own closed testing only" — the capture is AISI's own blog (title S091.txt:1, date S091.txt:13, publisher statement S091.txt:45 "The AI Security Institute is a research organisation within the Department of Science, Innovation and Technology."), i.e. first-party self-report throughout; entry :12-13 attributes every figure to AISI.

## 8. Adjacency text the lane should correct (text only — nothing edited)

C1 — PROVINCE.md:205, scope-limit clause pointer. Text now: "scope limit: the statements of one government institute about its own closed testing only — LLM evaluation method stays adjacent to kengaku (Adjacent above), the underlying runs are unpublished, and METR's software-engineering doubling and the Frontier AI Trends Report stay unabsorbed". The clause is true but the reader cannot resolve the named adjacency from kengaku's PROVINCE.md (0 hits for METR / time horizon / agent-time-horizon / UK AISI there; see §7). Suggested text for the lane to consider, as an appended factual annotation in the lane's own r52 style: "…LLM evaluation method stays adjacent to kengaku (Adjacent above): the METR-style human-duration time-horizon measure is kengaku's (kengaku corpus/README.md:59 and :312; kengaku SOURCES rows S013/S014), and kengaku's PROVINCE.md names only the domain ('LLM/model research & evaluation', kengaku PROVINCE.md:3)". (Append-only; the existing line keeps its number.)

C2 — corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:77-78 (and corpus/lessons/round-58.md:38). Text now: "the linked Frontier AI Trends Report (S091.txt:2) is named and not opened: a lead, not a row." The capture line holds only the link label — S091.txt:2 is exactly `Read the Frontier AI Trends Report`, with no URL in the file (the capture contains no http(s) URL on that line and no metr.org/aisi second URL anywhere). The lane's registry has no corresponding lead line: `grep -c 'Trends' corpus/SOURCES.md` → 0, and the Leads (unopened) block is corpus/SOURCES.md:138-148 with 8 bullets (Big Sleep, ISO/IEC 29147+30111, UK AI Security Institute, GitHub repository security advisories REST API, NVD API 2.0 response-schema, OpenSSF Scorecard, CISA ADP list page) — none is the Trends Report. Suggested text: "named in the capture's link label (S091.txt:2, no URL captured) and not opened: not a row, and no registry lead line — the registry carries it only as a mention inside the S091 row (corpus/SOURCES.md:98)". Either that, or add the lead line to corpus/SOURCES.md §Leads — but the capture has no URL to record, so the annotation form is the lower-risk edit.

C3 — the missing in-lane adjacency annotation for the AISI cyber-range prior mention (§5). Suggested text, appended to PROVINCE.md in the lane's r52 form (PROVINCE.md:194): "[r58 adjacency annotation, appended 2026-11-03, factual, append-only] The F39 entry's cyber-range claim (corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:60-69) names AISI's report of a newer Mythos Preview checkpoint completing both cyber ranges (S091.txt:34-35). One byte inside the lane's own corpus and outside the F39 entry's scope already named the same surface in the second hand: corpus/source-snapshots/round-24/S012.txt:32 (Anthropic's Project Glasswing post, published May 22, 2026): 'The UK's AI Security Institute reports that Mythos Preview is the first model to solve both of their cyber ranges …'. The two statements are consistent (the round-24 text reflects the earlier AISI reporting; the F39 text the newer checkpoint), and no sibling lane holds either surface. Recorded here as an adjacency fact, not as a change to the F39 entry."

C4 — cross-lane id ambiguity, for the orchestrator rather than the lane's files: kasegi's S091 is the AISI blog; kengaku's S091 is the Agentic Benchmark Checklist (arXiv 2507.02825) whose fetched bytes carry five "UK AISI" affiliations (kengaku corpus/evidence/round53/fetched/C1PriceL1-general-best-practices.html:297, :302, :307, :312; registry row kengaku corpus/SOURCES.md:104). Per-lane registries make this legal, but "S091" is ambiguous if quoted across lanes. (No file change proposed on either side; reported only.)

C5 — observation only, not a correction to kasegi: kengaku stores the same fetched bytes twice, and the second name misdescribes the content — `C1PriceScoutD-row-gcode-to-text__arxiv-2507.02825v1.html` has the identical sha256 98c7ee12059a143519b4f1ce3d51106c6d44114bc55e2aa997857c40540dbecc as `C1PriceL1-general-best-practices.html`, and its title is "Establishing Best Practices for Building Rigorous Agentic Benchmarks" (0 occurrences of "gcode"). kasegi is read-only on siblings and cannot touch it; reported to the orchestrator.

## 9. Verification commands a reader can re-run (all read-only)

Every number in this file comes from one of these:

1. `ls -d */PROVINCE.md | wc -l` → 21 ; `ls -d */PROVINCE.md | grep -vc '^kasegi-shokunin/'` → 20
2. `grep -nE 'AI Security Institute|AISI|time horizon|time-horizon|METR|Mythos|GPT-5\.5|cyber range|autonomous cyber' */PROVINCE.md | cut -d: -f1,2` → 2 lines (kasegi:205, mado:32)
3. `grep -niE '\bAI Security Institute\b|\bAISI\b|\btime[ -]horizons?\b|\bMETR\b|\bMythos\b|\bGPT-?5\.5\b|\bcyber ranges?\b|\bautonomous cyber\b' */PROVINCE.md | grep -v '^kasegi-shokunin/'` → no output, exit 1
4. the python host-word classifier over `*/PROVINCE.md` (re 'aisi|METR', case-insensitive) → 41 hits, 1 genuine
5. `for d in <20 siblings>; do for p in <9 tokens>; do grep -rIl -e "$p" "$d-shokunin/corpus/knowledge"; done; done` → 10 file listings, classified in §3.1
6. `for d in <20 siblings>; do grep -rIl -i 'AI Security Institute' …; grep -rIl 'aisi.gov.uk' …; done` → 0 hits in all 20 siblings
7. `grep -rIl 'UK AISI' <20 siblings>/corpus …` → 2 files, both kengaku (4 occurrences each)
8. `ls corpus/knowledge/*.md | wc -l` → 77 ; `grep -nE '…9 tokens…' corpus/knowledge/*.md | wc -l` → 32
9. `grep -cE '\bMETR\b' …` per sibling corpus file → host words classified in §3.1
10. `grep -rIn 'GPT-5\.5' corpus/` → 6 lines, all in captures (S091.txt ×5, S011.txt ×1), none in a knowledge file
11. `sed -n '32p' corpus/source-snapshots/round-24/S012.txt` → the AISI cyber-range sentence; `grep -rn 'S012.txt:32' corpus/ .ufo/waves/round-58/` → no output
12. `for p in '\bMETR\b' 'time[ -]horizon' 'agent-time-horizon' 'UK AISI'; do grep -cE "$p" kengaku-shokunin/PROVINCE.md; done` → 0 0 0 0
13. `sed -n '59p' kengaku-shokunin/corpus/README.md` ; `sed -n '312p' …` ; `grep -n '^| S013 \|^| S014 ' kengaku-shokunin/corpus/SOURCES.md` → the sibling owning sentences quoted in §1 and §6
14. `grep -c 'Trends' corpus/SOURCES.md` → 0 ; `sed -n '138,148p' corpus/SOURCES.md` → the 8 lead bullets, none the Trends Report
15. `python3 -c "…re.search('<title>'…)" kengaku-shokunin/corpus/evidence/round53/fetched/C1PriceL1-general-best-practices.html` → "Establishing Best Practices for Building Rigorous Agentic Benchmarks"; `grep -n 'UK AISI' <same file>` → 297, 302, 307, 312
16. `sha256sum` of the two kengaku fetched files → identical 98c7ee12059a143519b4f1ce3d51106c6d44114bc55e2aa997857c40540dbecc

Scratch cleanup: `/fast/scratch/hyaku/kasegi-r58/SiblingOverlap` (e1.txt, e1b.txt, final-evidence.txt, ct/) removed before yield; no leftover files; nothing written to the fleet root, to any sibling lane, or to L other than this file.

## 10. Working-tree note (concurrent repairs by another seat — not mine, not in the commit under test)

This seat's line citations are to the implementation commit 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b, which is what the seat scope names ("the implementation under test is landed at commit 18ddb05"). While this seat was running, another seat applied repairs to the lane working tree; `git -C L status --short` at the end of this seat showed `M corpus/SOURCES.md` and `M corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md` in addition to the pre-existing `M LOG.md`, `M SCORECARD.md`, `M corpus/QUALITY.md`. I did not write those files. Impact on the numbers in this file:

$ ls corpus/knowledge/*.md | wc -l ; grep -nE 'AI Security Institute|AISI|time horizon|time-horizon|METR|Mythos|GPT-5\.5|cyber range|autonomous cyber' corpus/knowledge/*.md | wc -l
77
32
$ (same two commands over `git archive 18ddb05 corpus/knowledge`, extracted to scratch)
77
32

Both counts are identical at the commit and in the working tree, so every hit count and per-pattern file list in §2–§4 stands for both. The only drift is line numbers inside the F39 entry (82 lines committed → 81 in the working tree):

| anchor | at 18ddb05 (cited above) | in the working tree at the time of this note |
|---|---|---|
| METR bullet | entry :76 | entry :74 |
| Adjacency bullet | entry :81-84 | entry :79-81 |
| Claim 4 heading | entry :60 | entry :58 |

The working tree's METR bullet additionally now reads "…4.2 months, which the report's footnote 3 gives excluding Mythos Preview (4 months with it)…" — i.e. another seat has already recorded the footnote-3 variant that §4 flags as a coverage matter for the C2 seats. Nothing in the sibling scan changes: the S091 registry row (corpus/SOURCES.md:98), the AISI lead line (:142 at the tip in both), the PROVINCE.md F39 line (:205) and the round-24 S012.txt:32 prior mention are all unchanged by those repairs; `grep -c 'Trends' corpus/SOURCES.md` is still 0, so correction C2 in §8 still applies to the working tree as well as to the commit. The adjacent-surface conclusions of §6 and §7 are unaffected — the boundary sentences quoted there live in PROVINCE.md:50, PROVINCE.md:205 and kengaku's corpus/README.md:59/:312, none of which the concurrent repairs touched.
