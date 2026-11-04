REFERENTS-HOLD

# ExecAnchors — R71 anchor-referent table for F41 / S093 (kasegi round-60 w1)

Scope: every free line anchor naming the round-60 capture in the three named surfaces — the
F41 entry, the S093 row of `L/corpus/SOURCES.md`, and the F41 row of `L/corpus/README.md` —
each printed beside its named capture line (first 160 chars) and judged against the sentence
it supports. **69 anchor occurrences judged, 0 mismatches, 0 off-by-one, script exit 0.**

Anchor census (independently counted; details in §2):

| surface | anchor form | count |
|---|---|---|
| `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md` (12 anchor-bearing lines: 10, 14, 16, 20, 22, 26, 28, 32, 34, 39, 40, 41) | `S093.txt:<n>` / `S093.txt:<n>-<m>` (50) + relative `, :<n>` continuations on entry:20 (3) | 53 |
| `corpus/SOURCES.md:100` (S093 row) | bare `L<n>` / `L<n>-L<m>` bound to the capture named in the same cell (the row contains 0 literal `S093.txt:<n>` strings) | 16 |
| `corpus/README.md:1005` (F41 row; also 993–1006 block and 1001 coverage row) | none — the row states 316/441, 178/95, 45/37 without line cites | 0 |

The 16 SOURCES anchors are the row's free line anchors under R71's "a SOURCES row" scope: the
`anchor` cell opens with `capture corpus/source-snapshots/round-60/S093.txt (40649 bytes, 283
lines, sha256 46f69d32…):` and then cites `L12-L14`, `L16`, `L40`, `L51`, `L55`, `L56`, `L60`,
`L61`, `L65`, `L68`, `L71`, `L74`, `L82`, `L88`, `L16` (Q12,Q13) and `L281` (Q14,Q15). Each was
resolved against that capture and judged.

All 69 rows carry the referent of the sentence they support; no anchor is one line off. The
15 pinned Q ids cited in the entry and the row agree with the round-60 manifest anchors
(29 Q-cite occurrences, `Q_CHECK mismatches=0`).

Files changed: this file only (`L/.ufo/waves/round-60/w1/ExecAnchors.md`). Lane read-only; no
git/jj mutation against the lane; no tool installs or upgrades; no credential material; scratch
deleted at yield (§8).

---

## 1. Lane state and capture identity (all commands absolute)

The assignment names commit `7f7dd26` as lane HEAD; the lane advanced during the wave, so I
verified blob identity instead of trusting the mutable HEAD. At measurement HEAD was
`228118a8cfba679c1d97841aa3af38e5ec83d84a` (log: `228118a` SCORECARD/LOG on top of `fb6a928`
lesson on top of `7f7dd26`). The three audited paths have byte-identical blobs at `7f7dd26`
and at HEAD, and the working tree is clean for them:

```
$ L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git -C "$L" rev-parse HEAD
228118a8cfba679c1d97841aa3af38e5ec83d84a

$ for p in corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md corpus/SOURCES.md corpus/README.md; do
    printf '%s\n  7f7dd26:%s\n  HEAD:%s\n' "$p" \
      "$(git -C "$L" rev-parse 7f7dd267283d2a16ca38d4cb05bed92165cb35cd:"$p")" \
      "$(git -C "$L" rev-parse HEAD:"$p")"; done
corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
  7f7dd26:e90315757b509ee61e41a5d9d716769731aaaac4
  HEAD:e90315757b509ee61e41a5d9d716769731aaaac4
corpus/SOURCES.md
  7f7dd26:b63a6cb8e783d1e57bdd59089420a8df73c4e4fc
  HEAD:b63a6cb8e783d1e57bdd59089420a8df73c4e4fc
corpus/README.md
  7f7dd26:7a7f52078faaf3c00184c605e36851913e51a756
  HEAD:7a7f52078faaf3c00184c605e36851913e51a756

$ git -C "$L" diff --quiet 7f7dd267283d2a16ca38d4cb05bed92165cb35cd..HEAD -- \
    corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md corpus/SOURCES.md corpus/README.md
$ echo quiet_exit=$?
quiet_exit=0

$ git -C "$L" status --porcelain -- <same three paths>
(no output)

$ sha256sum "$L/corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md" \
            "$L/corpus/SOURCES.md" "$L/corpus/README.md"
77e200f8663d623f3b93410193c09d42bee0c5c42d151cff47ab40772b2253e1  .../project-zero-fuzzilli-vs-bigsleep-comparison.md
c952fe07b7bf3a52bde8fd5d5b638e60e4d6e4e34f85250f30a6b5acaf956b52  .../SOURCES.md
3e1b0081bf826e77c2d98994a24e60b6fd7e9f45fa6d1876c571b6c6f0752bc6  .../README.md
```

Capture identity — the sha256 and line count match the C2 frozen values and the manifest:

```
$ sha256sum "$L/corpus/source-snapshots/round-60/S093.txt"
46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96  .../S093.txt
$ wc -l "$L/corpus/source-snapshots/round-60/S093.txt"
283 .../S093.txt
```

Pointer lines: entry anchor-bearing lines 10, 14, 16, 20, 22, 26, 28, 32, 34, 39, 40, 41
(`grep -n 'S093\.txt:' entry | cut -d: -f1`); `SOURCES.md:100` (`grep -n '^| S093 |'`);
`README.md:1005` (`grep -n '^| F41 |'`).

## 2. Anchor census (independent of the judge script)

```
$ grep -o 'S093\.txt:[0-9]\+\(-[0-9]\+\)\?' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md | wc -l
50
$ grep -o ', :[0-9]\+' corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md | wc -l
3
$ sed -n '100p' corpus/SOURCES.md | grep -o '\bL[0-9]\+\(-L\?[0-9]\+\)\?' | wc -l
16
$ sed -n '990,1006p' corpus/README.md | grep -oE 'S093\.txt:[0-9]+|S093\.txt:[0-9]+-[0-9]+' | wc -l
0
```

The extraction script's own census agrees and reports all resolves in range:

```
COUNT entry=53 sources=16 readme=0
OUT_OF_RANGE=0
```

Range anchors present: entry `S093.txt:33-34` (entry:22), `S093.txt:30-34` (entry:39) and
`S093.txt:53-68` (entry:28); no range anchor in the SOURCES row or README row. Relative
anchors: `:28`, `:31`, `:34`, all on entry:20 continuing `S093.txt:27`, `:30`, `:33`.

## 3. Scripts and run

Scratch: `S=/fast/scratch/hyaku/kasegi-r60/ExecAnchors` (absolute paths; `TMPDIR=$S`; cwd=$S).

```
$ sha256sum "$S/extract.py" "$S/judge.py" "$S/extract.out" "$S/judge.out"
4f001893b0e01c606bb5764ed5528823b2abd3e1c2e6e89a581506366050b60e  .../extract.py
8b9dbf35814fa00e22989ba592cb65f68a91c045c7e62939a59d45bc24d08b01  .../judge.py
26e60ce499439fb3decc5ba69a94f5dbacb7f0568e43b87dd583b3efa88b51e4  .../extract.out
97fbb311221fd420308ba4a0142465e5a9979f764e42ec0e20f1b58f17a2e216  .../judge.out

$ cd "$S" && TMPDIR="$S" python3 extract.py > extract.out 2>&1; echo "exit=$?"
exit=0
$ cd "$S" && TMPDIR="$S" python3 judge.py > judge.out 2>&1; echo "exit=$?"
exit=0
```

The judge script's exit semantics: 0 = every anchor's referent is on the named line; 1 = at
least one mismatch (off-by-one diagnostics printed); 2 = structural mismatch between the
extracted occurrences and the expectation table. It printed `SUMMARY occurrences=69 expected=69
pass=69 fail=0 q_mismatch=0` and `EXIT=0`.

## 4. Anchor-referent table (verbatim judge output)

`line content` is the exact first 160 characters the script printed for the resolved capture
line(s); for the three ranges the endpoints are shown with the span size. `Q` is the pinned
quote id when the anchor carries one; `-` means a free anchor (or an unpinned member of a
multi-line cite).

| # | source | anchor | Q | resolved | cited line(s), first 160 chars | referent | verdict |
|---|---|---|---|---|---|---|---|
| 1 | entry:10 | S093.txt:12 | Q1 | L12 | L12: Fuzzers vs. AI: Comparing Fuzzilli and BigSleep on JavaScript Engines | post title | PASS |
| 2 | entry:10 | S093.txt:13 | - | L13 | L13: 2026-Oct-27 | publication date | PASS |
| 3 | entry:10 | S093.txt:14 | - | L14 | L14: Samuel Groß | byline | PASS |
| 4 | entry:10 | S093.txt:16 | - | L16 | L16: Project Zero compared two automated tools used by Google to find vulnerabilities in Chrome’s JavaScript engine, V8, on a regular basis. Fuzzilli is a generative | two automated tools ... on a regular basis | PASS |
| 5 | entry:14 | S093.txt:22 | - | L22 | L22: For this blog post, we will limit ourselves to two concrete systems: Fuzzilli, a JavaScript engine fuzzer, and BigSleep, an agentic bug finding system. Both of  | scope sentence: two systems | PASS |
| 6 | entry:14 | S093.txt:23 | - | L23 | L23: We also limit ourselves to V8 as a target, a high-performance JavaScript and WebAssembly engine with a sophisticated and mature testing and fuzzing setup. In pa | target sentence: V8 | PASS |
| 7 | entry:14 | S093.txt:16 | - | L16 | L16: Project Zero compared two automated tools used by Google to find vulnerabilities in Chrome’s JavaScript engine, V8, on a regular basis. Fuzzilli is a generative | LLM-based bug finding system | PASS |
| 8 | entry:14 | S093.txt:22 | - | L22 | L22: For this blog post, we will limit ourselves to two concrete systems: Fuzzilli, a JavaScript engine fuzzer, and BigSleep, an agentic bug finding system. Both of  | production pipelines on newly added code | PASS |
| 9 | entry:14 | S093.txt:22 | - | L22 | L22: For this blog post, we will limit ourselves to two concrete systems: Fuzzilli, a JavaScript engine fuzzer, and BigSleep, an agentic bug finding system. Both of  | Fuzzilli many instances / BigSleep once per day | PASS |
| 10 | entry:16 | S093.txt:22 | - | L22 | L22: For this blog post, we will limit ourselves to two concrete systems: Fuzzilli, a JavaScript engine fuzzer, and BigSleep, an agentic bug finding system. Both of  | scope sentence | PASS |
| 11 | entry:16 | S093.txt:23 | - | L23 | L23: We also limit ourselves to V8 as a target, a high-performance JavaScript and WebAssembly engine with a sophisticated and mature testing and fuzzing setup. In pa | target sentence | PASS |
| 12 | entry:20 | S093.txt:26 | - | L26 | L26: This is the simplest part to analyze, although with some caveats we’ll see in a bit. The basic idea is to query issues from Chromium’s bugtracker (where V8 bugs | six months April-September 2026 | PASS |
| 13 | entry:20 | S093.txt:27 | - | L27 | L27: Fuzzilli: hotlistid:5433121 created:2026-04-01..2026-09-30 | Fuzzilli hotlist query | PASS |
| 14 | entry:20 | :28 | - | L28 | L28: BigSleep: hotlistid:8067258 created:2026-04-01..2026-09-30 | BigSleep hotlist query | PASS |
| 15 | entry:20 | S093.txt:30 | - | L30 | L30: Fuzzilli: 316 | Fuzzilli raw 316 | PASS |
| 16 | entry:20 | :31 | - | L31 | L31: BigSleep: 441 | BigSleep raw 441 | PASS |
| 17 | entry:20 | S093.txt:33 | - | L33 | L33: Fuzzilli: 178 | Fuzzilli type:vuln 178 | PASS |
| 18 | entry:20 | :34 | - | L34 | L34: BigSleep: 95 | BigSleep type:vuln 95 | PASS |
| 19 | entry:20 | S093.txt:40 | Q3 | L40 | L40: So in terms of vulnerabilities, it’s roughly a tie (small advantage BigSleep) at the moment: 45 vs. 37. | actionable tie 45 vs 37 | PASS |
| 20 | entry:20 | S093.txt:16 | Q2 | L16 | L16: Project Zero compared two automated tools used by Google to find vulnerabilities in Chrome’s JavaScript engine, V8, on a regular basis. Fuzzilli is a generative | summary pair 45 vs 37, 25% overlap | PASS |
| 21 | entry:20 | S093.txt:51 | Q4 | L51 | L51: Again, looking at just the actionable vulnerability reports (likely the best measure), we see an overlap of roughly 25% (20 out of a total of 81), with a slight | production overlap 20/81 | PASS |
| 22 | entry:22 | S093.txt:33-34 | - | L33-L34 | L33: Fuzzilli: 178 / L34: BigSleep: 95 | narrowing 178 / 95 | PASS |
| 23 | entry:22 | S093.txt:40 | - | L40 | L40: So in terms of vulnerabilities, it’s roughly a tie (small advantage BigSleep) at the moment: 45 vs. 37. | actionable 45 vs 37 | PASS |
| 24 | entry:22 | S093.txt:41 | - | L41 | L41: This naturally raises the question of cost: how expensive is each of the two approaches and what does that mean in terms of cost-per-bug? Unfortunately, it’s ch | no cost-per-bug comparison at this stage | PASS |
| 25 | entry:26 | S093.txt:55 | - | L55 | L55: We start with a list of historic Fuzzilli bugs (from early 2023 until mid-2026) by querying the bug tracker hotlist. This gives us around 1150 raw bugs. | ~1150 raw bugs | PASS |
| 26 | entry:26 | S093.txt:56 | - | L56 | L56: We restrict this to only type:vulnerability as these are the types of bugs we care most about and will remove some “noise” as above. We are left with roughly 60 | ~600 vulnerabilities | PASS |
| 27 | entry:26 | S093.txt:60 | - | L60 | L60: We end up with 132 historic bugs. | 132 historic bugs | PASS |
| 28 | entry:26 | S093.txt:61 | Q5 | L61 | L61: We now perform some deduplication similar to what we did above to identify implicit duplicates, which we remove. This leaves us with a final number of 112 bugs. | final 112 bugs | PASS |
| 29 | entry:26 | S093.txt:65 | Q6 | L65 | L65: We now run the agent for 25 attempts on each commit. The agent is asked to find bugs related to the commit and prove their existence by writing a testcase that  | 25 attempts per commit | PASS |
| 30 | entry:26 | S093.txt:65 | - | L65 | L65: We now run the agent for 25 attempts on each commit. The agent is asked to find bugs related to the commit and prove their existence by writing a testcase that  | Gemini 3.6 flash | PASS |
| 31 | entry:26 | S093.txt:71 | Q8 | L71 | L71: For the model used in this experiment (Gemini 3.6 flash), the knowledge cutoff date is March 2026. Combining that with the fact that in early 2026, Chrome bugs  | March 2026 knowledge cutoff | PASS |
| 32 | entry:26 | S093.txt:68 | Q7 | L68 | L68: Starting from just the commits that (likely) introduced the bugs, BigSleep was able to re-discover ~62% of the original bugs, while finding a different (but by  | re-discovery ~62% / ~12% / 26% | PASS |
| 33 | entry:26 | S093.txt:71 | - | L71 | L71: For the model used in this experiment (Gemini 3.6 flash), the knowledge cutoff date is March 2026. Combining that with the fact that in early 2026, Chrome bugs  | no significant memorization pre-2026 | PASS |
| 34 | entry:26 | S093.txt:82 | Q10 | L82 | L82: Running these two experiments with only 5 attempts per bug (instead of the 25 used in the main experiment), the agent re-discovered 10 additional bugs in total: | 10 = 8 + 7 follow-up bugs | PASS |
| 35 | entry:26 | S093.txt:84 | - | L84 | L84: So the share of “correct” bugs found climbs to ~70%, and we find some kind of bug for ~84% of starting points. However, for fairness it should be noted that equ | equivalent fuzzer tweaks caution | PASS |
| 36 | entry:26 | S093.txt:88 | Q11 | L88 | L88: In our experiment, overlap was around 60% of historic Fuzzilli bugs (70% with additional runs that used different prompts). | experiment overlap ~60% (70%) | PASS |
| 37 | entry:28 | S093.txt:53-68 | - | L53-L68 | L53: The second way to measure the overlap is to run a dedicated experiment in which we try to re-discover bugs found by one system in the past using the other. Spec ... L68: Starting from just the commits that (likely) introduced the bugs, BigSleep was able to re-discover ~62% of the original bugs, while finding a different (but by  (+14 lines in span) | experiment span: setup -> result | PASS |
| 38 | entry:28 | S093.txt:84 | - | L84 | L84: So the share of “correct” bugs found climbs to ~70%, and we find some kind of bug for ~84% of starting points. However, for fairness it should be noted that equ | 'treated with some caution' | PASS |
| 39 | entry:28 | S093.txt:53 | - | L53 | L53: The second way to measure the overlap is to run a dedicated experiment in which we try to re-discover bugs found by one system in the past using the other. Spec | reverse direction difficult to set up | PASS |
| 40 | entry:32 | S093.txt:16 | Q12 | L16 | L16: Project Zero compared two automated tools used by Google to find vulnerabilities in Chrome’s JavaScript engine, V8, on a regular basis. Fuzzilli is a generative | 'fuzzing and LLMs are still complementary' | PASS |
| 41 | entry:32 | S093.txt:16 | Q13 | L16 | L16: Project Zero compared two automated tools used by Google to find vulnerabilities in Chrome’s JavaScript engine, V8, on a regular basis. Fuzzilli is a generative | 'We recommend vendors perform both' | PASS |
| 42 | entry:32 | S093.txt:281 | Q14 | L281 | L281: In this blog post, we’ve compared coverage-guided fuzzers with vulnerability-discovery agents that read and reason about the source code. Specifically, we’ve lo | 'the two approaches remain complementary ...' | PASS |
| 43 | entry:32 | S093.txt:90 | - | L90 | L90: Bugs that are difficult for a fuzzer to find are more likely to also be difficult to find for an agent, so there’s more overlap on “easy” bugs. | more overlap on easy bugs | PASS |
| 44 | entry:32 | S093.txt:91 | - | L91 | L91: The overlap seems to be smaller in the JIT Compilers and higher in the rest of the engine. | smaller overlap in JIT compilers | PASS |
| 45 | entry:32 | S093.txt:74 | Q9 | L74 | L74: While we do get a statistically significant result here (although not of particularly great magnitude), it actually points in the other direction! Bugs that are | hard for fuzzer => hard for AI agent | PASS |
| 46 | entry:32 | S093.txt:281 | Q15 | L281 | L281: In this blog post, we’ve compared coverage-guided fuzzers with vulnerability-discovery agents that read and reason about the source code. Specifically, we’ve lo | 'further model improvements' outlook | PASS |
| 47 | entry:34 | S093.txt:16 | Q13 | L16 | L16: Project Zero compared two automated tools used by Google to find vulnerabilities in Chrome’s JavaScript engine, V8, on a regular basis. Fuzzilli is a generative | recommendation sentence | PASS |
| 48 | entry:34 | S093.txt:281 | Q14 | L281 | L281: In this blog post, we’ve compared coverage-guided fuzzers with vulnerability-discovery agents that read and reason about the source code. Specifically, we’ve lo | conclusion sentence | PASS |
| 49 | entry:39 | S093.txt:41 | - | L41 | L41: This naturally raises the question of cost: how expensive is each of the two approaches and what does that mean in terms of cost-per-bug? Unfortunately, it’s ch | no cost-per-bug comparison | PASS |
| 50 | entry:39 | S093.txt:30-34 | - | L30-L34 | L30: Fuzzilli: 316 ... L34: BigSleep: 95 (+3 lines in span) | 316/441 vs 178/95 narrowing | PASS |
| 51 | entry:40 | S093.txt:53 | - | L53 | L53: The second way to measure the overlap is to run a dedicated experiment in which we try to re-discover bugs found by one system in the past using the other. Spec | reverse experiment direction statement | PASS |
| 52 | entry:41 | S093.txt:71 | - | L71 | L71: For the model used in this experiment (Gemini 3.6 flash), the knowledge cutoff date is March 2026. Combining that with the fact that in early 2026, Chrome bugs  | Gemini 3.6 flash bound | PASS |
| 53 | entry:41 | S093.txt:71 | - | L71 | L71: For the model used in this experiment (Gemini 3.6 flash), the knowledge cutoff date is March 2026. Combining that with the fact that in early 2026, Chrome bugs  | may differ for other/future models | PASS |
| 54 | sources:100 | L12-L14 | Q1 | L12-L14 | L12: Fuzzers vs. AI: Comparing Fuzzilli and BigSleep on JavaScript Engines / L13: 2026-Oct-27 / L14: Samuel Groß | title / date / byline | PASS |
| 55 | sources:100 | L16 | Q2 | L16 | L16: Project Zero compared two automated tools used by Google to find vulnerabilities in Chrome’s JavaScript engine, V8, on a regular basis. Fuzzilli is a generative | production numbers 45 vs 37 | PASS |
| 56 | sources:100 | L40 | Q3 | L40 | L40: So in terms of vulnerabilities, it’s roughly a tie (small advantage BigSleep) at the moment: 45 vs. 37. | actionable pair 45 vs 37 | PASS |
| 57 | sources:100 | L51 | Q4 | L51 | L51: Again, looking at just the actionable vulnerability reports (likely the best measure), we see an overlap of roughly 25% (20 out of a total of 81), with a slight | production overlap 20/81 | PASS |
| 58 | sources:100 | L55 | - | L55 | L55: We start with a list of historic Fuzzilli bugs (from early 2023 until mid-2026) by querying the bug tracker hotlist. This gives us around 1150 raw bugs. | ~1150 raw | PASS |
| 59 | sources:100 | L56 | - | L56 | L56: We restrict this to only type:vulnerability as these are the types of bugs we care most about and will remove some “noise” as above. We are left with roughly 60 | ~600 vulnerabilities | PASS |
| 60 | sources:100 | L60 | - | L60 | L60: We end up with 132 historic bugs. | 132 historic | PASS |
| 61 | sources:100 | L61 | Q5 | L61 | L61: We now perform some deduplication similar to what we did above to identify implicit duplicates, which we remove. This leaves us with a final number of 112 bugs. | final 112 | PASS |
| 62 | sources:100 | L65 | Q6 | L65 | L65: We now run the agent for 25 attempts on each commit. The agent is asked to find bugs related to the commit and prove their existence by writing a testcase that  | 25 attempts | PASS |
| 63 | sources:100 | L68 | Q7 | L68 | L68: Starting from just the commits that (likely) introduced the bugs, BigSleep was able to re-discover ~62% of the original bugs, while finding a different (but by  | re-discovery ~62% | PASS |
| 64 | sources:100 | L71 | Q8 | L71 | L71: For the model used in this experiment (Gemini 3.6 flash), the knowledge cutoff date is March 2026. Combining that with the fact that in early 2026, Chrome bugs  | March 2026 cutoff | PASS |
| 65 | sources:100 | L74 | Q9 | L74 | L74: While we do get a statistically significant result here (although not of particularly great magnitude), it actually points in the other direction! Bugs that are | difficulty result | PASS |
| 66 | sources:100 | L82 | Q10 | L82 | L82: Running these two experiments with only 5 attempts per bug (instead of the 25 used in the main experiment), the agent re-discovered 10 additional bugs in total: | prompt follow-up 10 = 8 + 7 | PASS |
| 67 | sources:100 | L88 | Q11 | L88 | L88: In our experiment, overlap was around 60% of historic Fuzzilli bugs (70% with additional runs that used different prompts). | experiment overlap ~60% | PASS |
| 68 | sources:100 | L16 | Q12, Q13 | L16 | L16: Project Zero compared two automated tools used by Google to find vulnerabilities in Chrome’s JavaScript engine, V8, on a regular basis. Fuzzilli is a generative | complementarity + recommendation | PASS |
| 69 | sources:100 | L281 | Q14, Q15 | L281 | L281: In this blog post, we’ve compared coverage-guided fuzzers with vulnerability-discovery agents that read and reason about the source code. Specifically, we’ve lo | conclusion + outlook | PASS |

Off-by-one diagnostics: `OFF_BY_ONE=0` (the script probes `n-1` and `n+1` whenever a needle is
missing from the named span; none was missing).

## 5. Range spans, every line printed (first 160)

`S093.txt:30-34` (entry:39 — raw counts, explanation, type-filtered counts):

```
L30: Fuzzilli: 316
L31: BigSleep: 441
L32: Small win for BigSleep. However, this includes all types of bugs, and BigSleep initially also found a lot of configuration and integration issues in V8, for exa
L33: Fuzzilli: 178
L34: BigSleep: 95
```

`S093.txt:53-68` (entry:28 — overlap-experiment setup through result):

```
L53: The second way to measure the overlap is to run a dedicated experiment in which we try to re-discover bugs found by one system in the past using the other. Spec
L54: In more detail, here is how the experiment is set up:
L55: We start with a list of historic Fuzzilli bugs (from early 2023 until mid-2026) by querying the bug tracker hotlist. This gives us around 1150 raw bugs.
L56: We restrict this to only type:vulnerability as these are the types of bugs we care most about and will remove some “noise” as above. We are left with roughly 60
L57: Next, we filter this list down to bugs that reproduce in the environment used by the agent. This involves two parts:
L58: Bugs that reproduce on an x64 debug+asan build of the d8 shell as provided by Chrome’s public build infrastructure. This is important because many bugs only rep
L59: Bugs that can be reproduced without special flags. The problem here is that fuzzers often set custom flags, either to enable in-development features (e.g. --exp
L60: We end up with 132 historic bugs.
L61: We now perform some deduplication similar to what we did above to identify implicit duplicates, which we remove. This leaves us with a final number of 112 bugs.
L62: For a realistic comparison, we then convert these bugs into “code review challenges” similar to the ones used by the production BigSleep pipeline. For that, we 
L63: We likely sometimes identify the wrong commit that is unrelated to the bug in question, making the task harder or even impossible.
L64: We only have one commit per bug, while in the real world, the agent might discover the bug from another, subsequent commit that touches a similar part of the co
L65: We now run the agent for 25 attempts on each commit. The agent is asked to find bugs related to the commit and prove their existence by writing a testcase that 
L66: Finally, we run some post-processing on the results to check if the agent found the “right” bug or an unrelated one. For that, we check that the testcase crashe
L67: Here are the results from the experiment:
L68: Starting from just the commits that (likely) introduced the bugs, BigSleep was able to re-discover ~62% of the original bugs, while finding a different (but by
```

`S093.txt:33-34` (entry:22 — the narrowing pair): `L33: Fuzzilli: 178` / `L34: BigSleep: 95`.

## 6. Q-anchor cross-check (entry/row cite vs manifest)

The judge script resolved every Q id cited beside an anchor through
`corpus/source-snapshots/round-60/manifest.json` and compared its pinned anchor with the cited
line. 29 Q-cite occurrences, all OK:

```
Q_CHECK mismatches=0
Q1->12  Q2->16  Q3->40  Q4->51  Q5->61  Q6->65  Q7->68  Q8->71  Q9->74
Q10->82 Q11->88 Q12->16 Q13->16 Q14->281 Q15->281
```

The SOURCES row's multi-id citations (`L16 (Q12, Q13)`, `L281 (Q14, Q15)`) split and both ids
resolve to the same line as the row's anchor.

## 7. Judgment notes and residual risk

- All 69 occurrences carry their sentence's stated referent (title/date/byline; scope and
  target sentences; the six-month window and both hotlist queries; both successive count
  triples 316/441 and 178/95; the 45-vs-37 pair and 20/81 overlap; the sample ladder
  1150→~600→132→112; 25 attempts; Gemini 3.6 flash / March 2026 cutoff; the re-discovery
  shares ~62%/~12%/26%; the 10 = 8 + 7 follow-up; the ~60%/~70% experiment overlap; the
  ~25% and ~60% overlaps; the difficulty result; the complementarity/recommendation/outlook
  sentences).
- The only non-verbatim point is entry:40 `The reverse experiment was not run (S093.txt:53)`:
  L53 carries the reverse-direction statement and its "more difficult to set up" reason (the
  entry quotes that clause verbatim on entry:28), so the anchor names the referent line; the
  "not run" is the entry's inference and is not a line-anchor defect. Judged HOLD.
- The SOURCES row uses bare `L<n>` anchors after declaring the capture path in the same cell;
  this seat judged those 16 as the row's free line anchors (R71's SOURCES-row scope). The row
  contains no literal `S093.txt:<n>` string, and the README F41 row contains no line anchor
  at all — recorded as zero, not as a missing anchor.
- Residual: the check is phrase-presence on the named line plus a per-row semantic reading; it
  does not re-verify the underlying post's claims. All three range spans resolve in-bounds
  (1–283) and their endpoint referents are printed in §5.

## 8. Hygiene

- Files written: `W/ExecAnchors.md` only. No lane file, ledger, claims file, SOURCES/README/
  PROVINCE/QUALITY, knowledge file or instrument was edited; no `git add`/commit/stash/
  checkout/switch/reset/pull/push and no jj command was run against the lane (read-only git
  only). No sibling lane or fleet-root file touched.
- Tool installs/upgrades: none (python3 3.14.8 from the host sufficed; no package manager was
  invoked).
- No credential material (no secret, token, cookie, session value or `op://` reference) is
  written to this file.
- Scratch `S=/fast/scratch/hyaku/kasegi-r60/ExecAnchors` deleted after this file was written;
  no leftover. Script hashes are recorded in §3 so the run is reproducible from the commands.
