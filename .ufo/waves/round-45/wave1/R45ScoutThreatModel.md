VERDICT: INFO

The Linux Kernel threat model bounds what F27 may call a security bug, and it bounds only the impact half of the AI-report duties. It does not change the four frozen cores. It deserves its own SOURCES row (proposed below as S073, not written).

## What was opened

Assigned page `https://docs.kernel.org/process/threat-model.html`, reached from the security-bugs doc. S071 is the RST capture of that doc (`corpus/source-snapshots/round-45/S071.txt`). Its rendered HTML links the sibling five times. Body links sit on the qualification sentence, the AI impact sentence, and the AI “read this first” sentence.

Command:

```
curl -fsSL -A 'kasegi-r45-scout/1.0' -o threat-model.rst.txt -w 'rst_http=%{http_code} rst_url=%{url_effective} rst_bytes=%{size_download}\n' 'https://docs.kernel.org/_sources/process/threat-model.rst.txt'
curl -fsSL -A 'kasegi-r45-scout/1.0' -o threat-model.html -w 'html_http=%{http_code} html_url=%{url_effective} html_bytes=%{size_download}\n' 'https://docs.kernel.org/process/threat-model.html'
curl -fsSL -A 'kasegi-r45-scout/1.0' -o security-bugs.html -w 'sec_http=%{http_code} sec_url=%{url_effective} sec_bytes=%{size_download}\n' 'https://docs.kernel.org/process/security-bugs.html'
sha256sum threat-model.rst.txt threat-model.html security-bugs.html
```

Printed:

```
rst_http=200 rst_url=https://docs.kernel.org/_sources/process/threat-model.rst.txt rst_bytes=12031
html_http=200 html_url=https://docs.kernel.org/process/threat-model.html html_bytes=23132
sec_http=200 sec_url=https://docs.kernel.org/process/security-bugs.html sec_bytes=33621
2ca392f6b448b6ff39a6c7bbeab133f0c005470cd19a026bb4cbe59a7df6b30b  threat-model.rst.txt
45caf924cd9f4780b13690eadc30a7956ed1be832aace6093bc80ab5d426f7e3  threat-model.html
174a89d065a58c462c5b398255969fbfdd1d300ddb30f95b27959ddbd2980cb2  security-bugs.html
```

Header GET of the assigned URL printed `HTTP/2 200`, `content-type: text/html; charset=utf-8`, `last-modified: Sun, 18 Oct 2026 23:32:42 GMT`, `date: Wed, 28 Oct 2026 21:03:19 GMT`, `content-length: 23132`. Header GET of the RST source printed `HTTP/2 200`, `content-type: text/plain; charset=utf-8`, `last-modified: Sun, 30 Aug 2026 21:38:14 GMT`, `date: Wed, 28 Oct 2026 21:04:09 GMT`, `content-length: 12031`.

Sibling anchors printed from `security-bugs.html`:

```
L82 href=threat-model.html text='The Linux Kernel threat model'
L258 href=threat-model.html text='The Linux Kernel threat model, and ought to have been sent through'
L364 href=threat-model.html text='of the kernel’s threat model (see The Linux Kernel threat model)'
L395 href=threat-model.html text='assistant read this file and The Linux Kernel threat model before proceeding, and have it'
```

Those three body lines are the rendered form of `S071.txt:84-85`, `S071.txt:199`, and `S071.txt:233`. S071 names the sibling at those lines and nowhere else (`s071_threat_lines [85, 199, 233]`).

## Frozen cores are unchanged

`r45-c2-gate.py` cores are the 7-day embargo ceiling, “treat it as public”, “Binary-only executables are not accepted”, and “cannot be reproduced, it is not exploitable”. Whole-token scan of `threat-model.rst.txt` (240 lines) and of the rendered HTML article text:

```
pat='\bAI\b' hits=0
pat='embargo' hits=0
pat='calendar days' hits=0
pat='Binary-only' hits=0
pat='treat it as public' hits=0
pat='reproducer' hits=0
pat='\bLLM\b' hits=0
pat='assistant' hits=0
```

The HTML plain-text scan printed the same zeros, except `embargo` hits=1. The window is sidebar chrome, not this article: `bugs The Linux Kernel threat model CVEs Embargoed hardware issues Maintainer informatio`. HTML headings of the article are only “The Linux Kernel threat model”, “The kernel’s responsibilities”, and “What classes of problems are not considered vulnerabilities”.

So the page does not restate, tighten, or relax the embargo ceiling, the “treat it as public” duty, the binary-only refusal, or the sentence “if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug” (`S071.txt:41-43`).

## It bounds “what counts as a security bug”

S071’s qualification section does not contain the boundary. It defers. Located S071 quotes (≤25 words):

- `S071.txt:83-84` (23 words): “just regular bugs that have been improperly qualified as security bugs due to a lack of awareness of the Linux kernel's threat model”
- `S071.txt:89-90` (20 words): “urgent bugs that grant an attacker a capability they are not supposed to have on a correctly configured production system”
- `S071.txt:92-93` (13 words): “consider whether the issue actually crosses a trust boundary on such a system”

The operative test is only on the sibling page. Each sentence below is ≤25 words, present in the RST at the cited lines, and the rendered HTML check printed `YES` for each. The same phrases are absent from S071.

Do-nothing contrast, re-run against the pinned snapshot and the fetched RST:

```
s071_has=False rst_has=True phrase='constitute security breaches'
s071_has=False rst_has=True phrase='affects actively maintained versions'
s071_has=False rst_has=True phrase='already possessing the privileges required'
s071_has=False rst_has=True phrase='not realistically\n    reproducible on a production system'
```

Located threat-model quotes:

- `threat-model.rst.txt:94` (11 words): “Bugs that permit to violate the principles above constitute security breaches.”
- `threat-model.rst.txt:95-96` (15 words): “bugs that permit one violation only once another one was already achieved are only weaknesses.”
- `threat-model.rst.txt:98-99` (12 words): “a failure of these extra protections do not constitute a vulnerability alone.”
- `threat-model.rst.txt:104-105` (11 words; source has `**NOT**`): “the following classes of problems are NOT considered Linux Kernel vulnerabilities.”
- `threat-model.rst.txt:114-115` (18 words): “For a bug to qualify as a vulnerability, it must be demonstrated that it affects actively maintained versions.”
- `threat-model.rst.txt:144-145` (18 words): “actions performed by a user already possessing the privileges required to perform that action or modify that state”
- `threat-model.rst.txt:168-170` (20 words): “information leaks based on probabilistic approaches that are prone to measurement noise and not realistically reproducible on a production system.”
- `threat-model.rst.txt:207-208` (16 words): “Leaks of kernel memory addresses/pointers do not constitute an immediately exploitable vector and are not vulnerabilities”
- `threat-model.rst.txt:239-240` (17 words): “Any issue that can be mitigated by setting proper permissions and limits doesn't qualify as a vulnerability.”
- `threat-model.rst.txt:231-232` (16 words): “Issues that require physical access to the machine, hardware modification, or the use of specialized hardware”
- `threat-model.rst.txt:233-234` (18 words): “are out of scope unless the system is explicitly configured with technologies meant to defend against such attacks”

How that bounds S071:89-93, without rewriting S071:41-43:

- “capability they are not supposed to have” stops at a user who already holds that privilege (`:144-145`). A second step after a boundary was already crossed is a weakness, not a breach (`:95-96`).
- “correctly configured production system” excludes end-of-life trees unless the bug is shown on actively maintained versions (`:114-115`). The section from `:110` also sets aside staging and experimental configs, debug-only features, and out-of-tree forks. Those class names are in the RST; the sentences above are the quotable cores.
- “easily exploited” / imminent harm does not include lab-only probabilistic leaks (`:168-170`). That sentence is consistent with “unreproducible is not exploitable”. It does not replace it.
- Reproducible is not sufficient. Pointer leaks “are not vulnerabilities, though they must be reported and fixed” (`:207-209`). An issue mitigated by permissions and limits “doesn't qualify as a vulnerability” (`:239-240`).

## It bounds AI-report duties only at impact evaluation

The publicity rule stays S071-only. `S071.txt:95-96` (16 words): “If you resorted to AI assistance to identify a bug, you must treat it as public”. Absent from the threat model, as the token scan shows.

Two S071 duties point at this page and have no other text for their content:

- `S071.txt:198-199` (11 words): “Many AI-generated reports lack an understanding of the kernel's threat model”
- `S071.txt:232-233` (10 words): “make the assistant read this file and threat-model.rst before proceeding”

Those duties mean an AI report may not label a threat-model exclusion (already privileged, actively-unmaintained-only, pointer leak, permission-mitigated, physical access) as a security bug. They do not add a procedure. Plain text, the four mandatory items, and “treat it as public” remain S071 sentences. S071:234 also sends the assistant to `coding-assistants.rst`. That page was not opened.

## Do-nothing control

Frozen control file `.ufo/waves/round-45/controls/freeze-controls.txt`, printed this session:

```
control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1 expect=RED got=RED
```

That line was read from the file. This seat did not re-run `r45-c2-gate.py`.

Registry do-nothing, re-run over `corpus/SOURCES.md`, `corpus/README.md`, and `corpus/knowledge/*.md`:

```
SOURCES rows=70 max=S070 S071=False S073=False
registry_readme_knowledge_kernel_hits=0
```

`threat-model`, `docs.kernel.org`, and `security-bugs` each had `files_with_hits=0` on that set. The pinned S071 snapshot likewise does not contain the breach sentences (the `s071_has=False` lines above). A citation that never leaves S071 can support the four frozen cores. It cannot locate the bound on “what counts as a security bug”.

Sibling draft `wave1/R45ScribeEntryC.draft/linux-kernel-security-bugs-reporting-process.md:51` says the uncaptured Documentation files, threat-model included, are ones on which “No statement in this entry depends”. That holds for the four cores that draft quotes from S071. It does not hold for the qualification section its own `source:` line names (`S071.txt:73-107` in Entry D’s header; Entry C’s source line names “What qualifies as a security bug”), because `S071.txt:83-85` defines the mis-qualification by reference to a file whose sentences are not in the snapshot.

## Proposal (not written)

Admit a new row. Do not fold these quotes into S071. `r45-c2-gate.py` G5 locates curly quotes only against `S071.txt` line windows; a threat-model sentence cited as `S071.txt:N` fails that limb. G5 does not scan a citation that names another snapshot.

Proposed id `S073`. `S071` and `S072` are the two ids the frozen `claims.json` `frontier_step` already assigns (`70 -> 72`). Current registry max is `S070`. Do not consume `S071`.

| cell | proposal |
|---|---|
| id | S073 |
| source | The Linux Kernel threat model — https://docs.kernel.org/process/threat-model.html |
| kind | docs |
| tier | A (the kernel project’s own statement of what it treats as a vulnerability, same publisher class as the frozen S071 row) |
| scope | The kernel’s breach-versus-weakness test and the classes it says are not vulnerabilities. Not the reporting procedure, the embargo clock, or the AI publicity rule. |
| anchor | RST capture of `https://docs.kernel.org/_sources/process/threat-model.rst.txt`, HTTP 200, 12031 bytes, sha256 `2ca392f6b448b6ff39a6c7bbeab133f0c005470cd19a026bb4cbe59a7df6b30b`, 240 lines, fetched 2026-10-28T21:04:09Z; quotes at rst lines 94, 95-96, 104-105, 114-115, 144-145. Rendered HTML of the assigned URL, sha256 `45caf924cd9f4780b13690eadc30a7956ed1be832aace6093bc80ab5d426f7e3`, Last-Modified Sun, 18 Oct 2026 23:32:42 GMT, contains those sentences. |
| teaches | Bound a “security bug” claim by the kernel’s own breach test and non-vulnerability classes. Do not treat the four S071 cores as restated here. |
| status | mined only after the L1 pins the snapshot under `corpus/source-snapshots/`. This seat did not write the row, the snapshot, or the manifest. |
| opened | 2026-10-28 |
| recheck | 90d. The rendered HTML is newer than the `_sources` RST (2026-10-18 vs 2026-08-30). |
| used-by | The F27 knowledge entry, and only if that entry quotes this snapshot under an S073 citation. Leave the entry’s opening `source:` line as `S071 — https://docs.kernel.org/process/security-bugs.html` (`r45-c2-gate.py` G2). Do not add a 65th knowledge file (`G6` requires 64). |

G1–G6 stay satisfiable if S073 is an extra registry row, the F27 source line stays S071, and no threat-model sentence is cited as `S071.txt`. This seat did not run `sources-census.sh`, so G7 on an extra row is untested.

## Limitations

- One live fetch on 2026-10-28. The bytes were checked in scratch and then removed. The sha256 values and the quotes above are the record. No corpus snapshot was written.
- RST Last-Modified (2026-08-30) and HTML Last-Modified (2026-10-18) differ. Every sentence quoted here was confirmed in both. A full article diff against a kernel git tree was not done. The L1 should re-fetch before pinning and should not assume the `_sources` RST and the HTML page stay in lockstep.
- The HTML `embargo` hit is the documentation sidebar (“Embargoed hardware issues”), not a sentence of this page.
- `coding-assistants.rst`, which S071:234 names for the AI work procedure, was not opened. This page adds no AI procedure of its own.
- The frozen do-nothing C2 line was printed from `freeze-controls.txt`. The counter was not re-run.
- Word counts drop `**` and `` `` before splitting on whitespace, matching `r45-c2-gate.py` `norm`.
