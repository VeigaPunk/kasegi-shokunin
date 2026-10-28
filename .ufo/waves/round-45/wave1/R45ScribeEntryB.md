VERDICT: DRAFT-READY

Scope: C2 entry drafter B, F27 (Linux kernel security-bugs reporting process). Draft only. Nothing was committed, nothing was placed in `corpus/knowledge/`, and no shared file (`corpus/README.md`, `corpus/SOURCES.md`, `MANIFEST.json`, `.ufo/state`) was touched. Scratch used: `/fast/scratch/hyaku/kasegi-r45/R45ScribeEntryB` (removed on exit). No tools were installed or upgraded.

## Finding 1 — the F27 draft is built

- Attacked/built: `.ufo/waves/round-45/wave1/R45ScribeEntryB.draft/linux-kernel-security-bugs-reporting-process.md` (about 1848 words; 10 table rows plus header; sections: Scope and decision rule, Observed questions, Overlap and novelty, Limits, Falsifiable package rule, Rejected over-generalization).
- Header, as written (`sed -n '1,5p'`):
  - `# Linux kernel security-bugs reporting process`
  - blank
  - `source: S071 — https://docs.kernel.org/process/security-bugs.html — sections ...`
  - `verified-at: 2026-10-28`
  - `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d`
- Layout note: the brief says "lines 1-4" but also lists five header items, and the house template has five lines (title, blank, source, verified-at, recheck). I followed the template. Frozen G2 checks the first eight lines, so either layout passes.

## Finding 2 — frozen counter G5 and G2 on the final draft (run by me, real counter code)

Command (harness in `/fast/scratch/hyaku/kasegi-r45/R45ScribeEntryB/harness.py`): it loads `corpus/instruments/r45-c2-gate.py` read-only and calls its `g2` and `g5` functions. The only substitution is `entry_path`, because the F27 README row is not on the tree yet (Finding 5). `DRAFT` points at the draft.

Output (final run):
- `G2 (True, 'source=1 verified-at=1 recheck=1')`
- `G5 (True, 'spans=24 located=24 failed=0 cores=4/4')`

Every span is printed by the harness as `PASS L<a>-<b>` with its normalised text. Verbatim lines from that run:
- `PASS L95-96 words=16 :: If you resorted to AI assistance to identify a bug, you must treat it as public`
- `PASS L310-311 words=21 :: for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days`
- `PASS L39-40 words=5 :: Binary-only executables are not accepted.`
- `PASS L41-43 words=19 :: By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug.`
- `PASS L20-21 words=10 :: with no version indication, your report will not be processed`
- `PASS L22-23 words=14 :: A stable identifier such as a commit ID or an exact version is required`
- `PASS L95-96 words=5 :: must treat it as public`

The four frozen cores (7-day ceiling, AI treated as public, binary-only refusal, unreproducible is not exploitable) each appear inside a located span.

## Finding 3 — defects found in my first draft and fixed (transparency)

First G5 run on the draft: `G5 (False, 'spans=21 located=20 failed=1 cores=3/4')`. Two real defects:
1. The fragment “the start of the release process” was cited to `S071.txt:310`, but the phrase runs into line 311. Fixed to `S071.txt:310-311`. Failing line printed by the harness: `FAIL L310-310 words=6 :: the start of the release process`.
2. The AI "treat it as public" sentence appeared only as unquoted paraphrase, so the core `treat it as public` was missing (`cores=3/4`). Fixed by adding the curly quote `“If you resorted to AI assistance to identify a bug, you must treat it as public” (`S071.txt:95-96`)` in the AI row of the table.

A third fix: one span had its citation after a separating word ("among them"), which breaks the adjacency rule. Reworded so `“or use of AI-based tools” (`S071.txt:116-117`)` stands immediately after its quote.

## Finding 4 — discriminating controls (the counter must fail on bad input)

- Control A, do-nothing draft (header lines only, no quotes): `G5 (False, 'spans=0 located=0 failed=0 cores=0/4')`.
- Control B, the 7-day cite moved from `S071.txt:310-311` to `S071.txt:309-310`: `G5 (False, 'spans=24 located=22 failed=2 cores=3/4')`, with `FAIL L309-310 words=21 :: for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days` and `FAIL L309-310 words=6 :: the start of the release process`.

So G5 does not pass on an empty draft, and it does fail on a one-line mis-cite.

## Finding 5 — self-check: each quote's line verified with `sed -n` on the pinned capture

Each range was printed with `sed -n 'a,bp' corpus/source-snapshots/round-45/S071.txt`. The line text matches the quote as printed:

| quote (entry) | cite | `sed -n` output (quoted) |
|---|---|---|
| 7-day ceiling + 14-day extension | 310-311 | `for up to 7 calendar days from the start` / `of the release process, with an exceptional extension to 14 calendar days` |
| deferral reason | 313-314 | `only valid reason for deferring the publication of a fix is to accommodate` / `the logistics of QA and large scale rollouts which require release` |
| postponement at request | 309-310 | `as soon as they become available, this may be postponed at the request of` / `the reporter or an affected party for up to 7 calendar days from the start` |
| AI must treat as public | 95-96 | `**If you resorted to AI assistance to identify a bug, you must treat it as` / `public**. While you may have valid reasons to believe it is not, the security` |
| AI public-list example | 114-115; 116-117 | `consider the issue as being public or trivial to discover (e.g. result of a` / `widely available automated vulnerability scanning tool that can be repeated by` / `anyone, or use of AI-based tools).` |
| reproducer kept private | 99; 100 | `case, do not publicly share a reproducer, as this could cause unintended harm;` / `just mention that one is available and maintainers might ask for it privately` |
| binary-only refusal | 39-40 | `instructions, file-system image etc).  Binary-only executables are not` / `accepted.  Working exploits are extremely helpful and will not be released` |
| unreproducible not security bug | 41-43 | `without consent from the reporter, unless they are already public.  By` / `definition if an issue cannot be reproduced, it is not exploitable, thus it` / `is not a security bug.` |
| version range (required) | 20-21; 22-23 | `will not be processed.  Note that a time-dependent version such as "latest` / `exact version is required.  Versions designating kernels not coming from` |
| required items | 17-18 | `information is helpful.  The following information are absolutely necessary in` / `**any** security bug report:` |
| desirable only | 49 | `In addition, the following information are highly desirable:` |
| description | 31-32 | `  * **description of the problem**: a detailed description of the problem, with` / `    traces showing its manifestation, and why you consider that the observed` |
| majority are regular bugs | 82-83 | `It turns out that the majority of the bugs reported via the security team are` / `just regular bugs that have been improperly qualified as security bugs due to` |
| security list scope | 89-90 | `The security list exists for urgent bugs that grant an attacker a capability` / `they are not supposed to have on a correctly configured production system, and` |
| linux-distros contrast (kernel side) | 342-344 | `security team and other teams is difficult since for the kernel security` / `team occasional embargoes (as subject to a maximum allowed number of` / `days) start from the availability of a fix, while for "linux-distros"` |
| linux-distros contrast (distros side) | 345-346 | `they start from the initial post to the list regardless of the` / `availability of a fix.` |
| fix publication: publicly known | 305-306 | `Once a robust fix has been developed, the release process starts.  Fixes` / `for publicly known bugs are released immediately.` |
| F15 fallback recipient | 169-170 | `maintainers, **and only in this case**, it's possible to send your report to` / `the Linux kernel security team only.  Your message will be triaged, and you` |
| plain text | 195-196 | `Please **always convert your report to plain text** without any formatting` / `decorations before sending it.` |
| AI reproducer must be tested | 209 | `validity of the report should be seriously questioned. Note that since the` |
| AI MUST list | 239-241 | `On top of that procedure, the AI assistant **MUST**:` / `1. Prepare a plain-text report explaining the problem. It must contain the` |
| security list not a disclosure channel | 302 | `The security list is not a disclosure channel.  For that, see Coordination` |
| version currency | 26-27 | `have already been fixed, so it is extremely important that vulnerabilities` / `are verified on recent versions (development tree or latest stable` |
| distro-kernel label | 23-24 | `exact version is required.  Versions designating kernels not coming from` / `kernel.org (such as distro kernels) are meaningless to maintainers and` |

Uncited curly spans, checked with a scan that treats a span as cited only if a `(`S071.txt:` or `(`<file>.md:` citation follows it immediately. The scan's last output: `'Every kernel bug may be embargoed for 7 days from the day it is report'` and `'An AI-found bug is publicly known, so its fix is released immediately.'`. These are the two "Rejected:" claims, written in the house style of the template (a rejected claim in curly quotes, as `coordinated-disclosure-timelines.md:33` does). They are not source quotes and are not checked by G5. The F04 quote (`ai-assisted-finding-validation.md:16`) carries its own file citation.

## Finding 6 — source recheck and G4 (read-only)

Command: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071`. Output:
- `S071:sha256 OK`
- `S071:Q1 OK normalized=markup-whitespace occurrences=1 anchor=310-ok`
- `S071:Q2 OK normalized=markup-whitespace occurrences=1 anchor=95-ok`
- `S071:Q3 OK normalized=markup-whitespace occurrences=1 anchor=39-ok`
- `S071:Q4 OK normalized=markup-whitespace occurrences=1 anchor=41-ok`
- `S071:Q5 OK normalized=markup-whitespace occurrences=1 anchor=20-ok`
- rc=0. Frozen `g4` returned `G4 (True, 'recheck-rc=0 quotes-ok=5 frozen-cores-missing=0')`.
- SHA-256 of the capture, recomputed: `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40` (matches the brief and the manifest).

## Finding 7 — overlap and novelty claims checked by grep

- Command: `grep -n -i -E "calendar day|security@kernel|linux-distros|kernel" corpus/knowledge/*.md`. Hits: `iso-29147-divergence-and-clause-crosswalk.md` (its own 7-day figure is a receipt acknowledgement, line 48: "the acknowledgement within 7 days as necessary (L1916)"), plus `cisa-bod-20-01-vdp-minimums.md` (30/180/270/90-day deadlines, unrelated). No existing entry holds the kernel's 7-day postponement ceiling, so that part is new.
- Command: `grep -n -i -E "required field|absolutely necessary|will not be processed|reproducer|version range" corpus/knowledge/*.md`. Hits only in `cve-json-record-format.md:86` (CNA rules, a schema) and `rfc-9116-security-txt.md:1,51` (standard-level REQUIRED fields). No existing entry holds a project's own mandatory report-field list, so that is new.
- F02, F04 and F15 were read in full (`corpus/knowledge/coordinated-disclosure-timelines.md`, `ai-assisted-finding-validation.md`, `vendor-third-party-finding-coordination.md`). The draft cites their line numbers for each overlap claim. The F04 claim that its only disclosure line is "any applicable program restriction or disclosure requirement" is at `ai-assisted-finding-validation.md:16`.

## Finding 8 — version claim not supported by the capture

The brief says the page is "versioned 7.3.0 at capture". Command: `grep -n '7\.3' corpus/source-snapshots/round-45/S071.txt`. Output: none (exit 1). The pinned capture carries no version label. The draft therefore records no page version and says so in Limits. I did not write "7.3.0" anywhere in the entry.

## Finding 9 — gates that need L1 integration (not my lane; flagged)

Run against the current tree (read-only):
- G1 needs the F27 row. `grep -n -E "^\| F27 " corpus/README.md` → exit 1, no output. Frontier rows currently run to F26 (`corpus/README.md:628`). Integration item for L1.
- G3 needs the SOURCES row S071. `grep -n -E "^ {0,3}\|\s*S071\s*\|" corpus/SOURCES.md` → no output. Integration item for L1.
- G6 (`knowledge=63`): the frozen count is 64. `G6 (False, 'knowledge=63')`. Landing the F27 entry in `corpus/knowledge/` brings it to 64 — consistent with the gate, but the draft has not been placed.
- G7 was not run (it depends on the SOURCES row and the `sources-census.sh` path).

The draft is not in `corpus/knowledge/`. The L1 owns placement, the README row and the SOURCES row.

## Finding 10 — frozen C1 controls and C1 repairs

Not in my assignment (C2 entry drafter B only). I did not touch `corpus/instruments/r45-routed-defects.py`, the C1 repairs, or the C1 counter.

## Limitations

- Evidence is the pinned RST capture (`corpus/source-snapshots/round-45/S071.txt`, from `docs.kernel.org/_sources/process/security-bugs.rst.txt`), not the rendered HTML at the canonical URL. The recheck confirms the pinned bytes and the five manifest quotes only. It does not confirm that the live page still reads the same.
- The harness substitutes only the F27 README lookup in `entry_path`; G5 and G2 logic are the frozen code. G1, G3, G6 and G7 were not run as passes, for the reasons in Finding 9.
- "Start of the release process" is not defined in S071.txt; the entry does not define it.
- The page cross-refers to documents not captured (`threat-model.rst`, `reporting-issues.rst`, `submitting-patches.rst`, `coding-assistants.rst`, the kres repository, `get_maintainer.pl`). The draft does not evaluate them.
- The quotes are curated spans, not a complete audit of the page. The table shows 10 rows, above the six required.
- The draft directs no probing, testing, scanning or submission against any target.
- No commit, push, or git/jj mutation was run. Scratch was removed on exit.

## Appendix — harness used for Findings 2 and 4 (embedded so the evidence is reproducible)

Run as `python3 harness.py` with `DRAFT_OVERRIDE` unset for the final draft, or set to a control file. Reads only; the frozen counter is loaded from the lane tree and only its `entry_path` lookup is replaced.

```python
import importlib.util, re, os
ROOT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
DRAFT = os.environ.get("DRAFT_OVERRIDE") or (ROOT + "/.ufo/waves/round-45/wave1/R45ScribeEntryB.draft/linux-kernel-security-bugs-reporting-process.md")
spec = importlib.util.spec_from_file_location("g", ROOT + "/corpus/instruments/r45-c2-gate.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
g.entry_path = lambda root: (DRAFT, "entry=draft-substitute")
body = open(DRAFT, encoding="utf-8").read()
snap = open(ROOT + "/corpus/source-snapshots/round-45/S071.txt", encoding="utf-8").read().splitlines()
spans = re.findall(r"“([^”]+)”\s*\(`?S071\.txt:(\d+)(?:-(\d+))?`?", body)
print("spans found by G5 regex:", len(spans))
for q, a, b in spans:
    a = int(a); b = int(b) if b else a
    window = g.norm(" ".join(snap[max(a - 1, 0):b])); nq = g.norm(q)
    ok = bool(nq) and len(nq.split()) <= 25 and nq in window
    print(f"{'PASS' if ok else 'FAIL'} L{a}-{b} words={len(nq.split())} :: {nq}")
print("G2", g.g2(ROOT)); print("G5", g.g5(ROOT))
```
