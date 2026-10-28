# R44Scout3 — C2 reject candidate: ISO/IEC 29147 catalog page

## Finding

**Reject** `https://www.iso.org/standard/72311.html` as a round-44 C2 source. It is the lane's own unopened lead for ISO/IEC 29147, and it is a plausible mistaken primary: F11 already says the lane does not hold the standard. The opened page is the ISO store record for **ISO/IEC 29147:2018** (Edition 2). It does not contain the standard.

Two independent gates fail.

**No primary authority for a 29147 requirement.** The static HTTP body has an abstract, a lifecycle, a price, and an empty preview modal. Visible text contains no `shall` / `must`. The preview hook is `openModal(72311)` into `<div id="obp-modal-body"></div>`, which is empty until `ObpReader.load()` runs. That script was not executed. The English PDF+ePub and paper offers are `data-price="179"` with currency `CHF` (`itemprop="price"` / `itemprop="priceCurrency"`).

**No unique lane scope for a new frontier.** The abstract's only relational sentence restates F11's outward-versus-in-house split and names no deadline, field, or clause. F11 already records that split from S041 and already requires the edition a source names (JPCERT/CC 2014, Cisco 2018). Bibliographic facts on this page (2014 labelled Withdrawn, 2018 labelled current, stage 90.92, successor `ISO/IEC AWI 29147`) are ISO's own and are not quoted in the F11 entries. They are not a checkable disclosure rule, so they do not open F26.

### Opened page

| field | value |
|---|---|
| URL | `https://www.iso.org/standard/72311.html` |
| fetched | 2026-10-28T18:59:57Z (`Date` and `Last-Modified` both that instant) |
| HTTP | 200, no redirect, `content-type: text/html;charset=UTF-8` |
| UA | `kasegi-shokunin/1.0` |
| bytes | 89224 |
| sha256 | `134bcdd1c6bcff47c35dd70bf3dbe2ab50e51652a903fc755eb5ca756ee158f3` |

`<h1>` text: `ISO/IEC 29147:2018` / `Information technology — Security techniques — Vulnerability disclosure`.

Quotes (whitespace-separated tokens; `ISO/IEC` counted as one token):

1. 17 words, abstract, fetched body line 852: "This document provides requirements and recommendations to vendors on the disclosure of vulnerabilities in products and services."
2. 17 words, abstract, fetched body line 859: "Other related activities that take place between receiving and disclosing vulnerability reports are described in ISO/IEC 30111."
3. 9 words, status callout, fetched body line 616: "This publication was last reviewed and confirmed in 2024." The next sentence on line 617 is "Therefore this version remains current." (5 words).
4. Lifecycle label, fetched body lines 922-923: section head `Withdrawn`, link text `ISO/IEC 29147:2014` (`href="/standard/45170.html"`).
5. Stage, fetched body line 879: "International Standard to be revised" with anchor text `90.92`. Line 933 repeats `Stage:` `90.92` `(To be revised)`.
6. Successor, fetched body lines 1191-1192: section head `Under development`, link text `ISO/IEC AWI 29147` (`href="/standard/92945.html"`), under the heading "Will be replaced by".

The six abstract bullets (fetched body lines 853-858) name topics — receiving reports, remediation disclosure, terms, concepts, policy considerations, Annex A/B examples — and do not state the guidelines.

### Why this is not a new frontier

Committed at HEAD `66314015122b9aa32dc40f2f1815df56624c26d1`:

- The URL is only the unopened lead, not a registry row: `corpus/SOURCES.md:105`.
- F11 is already admitted: `corpus/README.md:212` — "Treat 29147 as the vendor's outward-facing disclosure standard and 30111 as its internal handling process; record the edition a source names (JPCERT/CC compares against 2014, Cisco claims 2018".
- The division entry's ground is the JPCERT/CC 2026 guideline, not ISO: `corpus/knowledge/iso-29147-and-30111-division-of-labour.md:1` and `:11-14`. Cisco's 2018 alignment is already recorded at `:19` and the edition rule at `:42` and `:47`.
- The crosswalk already refuses a direct reading: `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:56` ("the paywalled ISO document is not independently held") and `:66` ("the lane does not hold the standard itself").

A `rg` for `iso.org/standard/72311` under `/home/vgpnk/Projects/shokunin` `**/SOURCES.md` matched no registry row. The lead line above is the only kasegi hit, and it sits outside the registry table.

### Falsifiable flip

Re-open only when a captured text of **ISO/IEC 29147:2018**, or of **ISO/IEC AWI 29147** once that document is published, contains one requirement sentence such that:

- `grep -F` of that sentence against `corpus/source-snapshots/round-26/S041.txt` prints no hit, and
- the sentence is not the outward-versus-in-house split already stated at `corpus/knowledge/iso-29147-and-30111-division-of-labour.md:9-14`, and
- that sentence is the load-bearing quote of a new frontier row, anchored to the capture.

The catalog URL stays rejected while a fresh GET of `https://www.iso.org/standard/72311.html` still serves the abstract, an empty `#obp-modal-body`, and no numbered clause. Repeating quotes 1-2 does not flip.

If a later run of the OBP reader (`project-id` 72311) returns a sample that contains such a sentence, the flip fires for that sentence. It still does not make this catalog URL the authority.

## Do-nothing discrimination

Frozen control `.ufo/waves/round-44/controls/do-nothing.txt:1-13` (base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`): admitted frontier 25, source rows 68, knowledge files 62, F26 absent. HEAD `6631401` is that base plus one commit (`round-44: freeze claims and validated wave`). Re-measured on committed HEAD, not the dirty worktree:

- `git show HEAD:corpus/README.md | grep -cE '^\| F[0-9]+ \| .* \| admitted \|'` → `25` (F01–F25 only)
- `git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `68`
- `git ls-tree -r --name-only HEAD corpus/knowledge | grep -c '\.md$'` → `62`

This reject does not admit F26, does not add a registry row, and does not add a knowledge file. A do-nothing replay still cannot reach C2's after-state. C1 was not re-counted here; the frozen control still says 8 routed defects and no r44 correction at the freeze.

The worktree is dirty with uncommitted `corpus/SOURCES.md` rows S069 (mined) and S070 (rejected) and an untracked `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`. Those are not committed, not this seat's candidate, and not evidence that C2's after-state has landed. `git grep S069 HEAD -- corpus/SOURCES.md` printed nothing.

## Limits

- `ObpReader` was not executed, so a client-side sample is unseen. The static modal body is empty (fetched body line 741).
- `Last-Modified` equals the fetch instant and the response sets a cookie, so the sha256 may not reproduce on a later GET. The quotes above are the stable part.
- Fetched body line 666 carries a broken offer URL `https://www.iso.org:-1/standard/72311.html`. That is a page defect. It is not the rejection reason.
- `HYAKU_SCRATCH` was unset in this process. Scratch was `/home/vgpnk/.hyaku/scratch/kasegi-r44/R44Scout3/` because that directory already held other round-44 seat scratch (`R44Conn3`, `R44Critic3`, `R44Mutant1`). `/home/vgpnk/.cache/hyaku-scratch/kasegi-r44/` also exists and was not used.
- No tool was installed. `RULES.md` was read. Pacman was not invoked.
- No git/jj mutation. No edit to `corpus/`, sibling repos, or operator config. Scratch removed on exit.

## Commands

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
→ 66314015122b9aa32dc40f2f1815df56624c26d1

git -C ... log --oneline 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a..HEAD
→ 6631401 round-44: freeze claims and validated wave

curl -sS -D headers.txt -o body.html -A 'kasegi-shokunin/1.0' -L --max-redirs 5 --max-time 45 \
  'https://www.iso.org/standard/72311.html'
→ curl_http=200 final=https://www.iso.org/standard/72311.html bytes=89224 redir=0
→ sha256 134bcdd1c6bcff47c35dd70bf3dbe2ab50e51652a903fc755eb5ca756ee158f3

git grep -n 'iso.org/standard/72311' HEAD -- corpus/SOURCES.md
→ HEAD:corpus/SOURCES.md:105 (leads bullet only)

git grep -n '^| F11 |' HEAD -- corpus/README.md
→ HEAD:corpus/README.md:212
```

Trailer (paths relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`):

- `.ufo/waves/round-44/wave1/R44Scout3.md`
- `.ufo/waves/round-44/controls/do-nothing.txt:1-13`
- `.ufo/waves/round-44/claims.json` C2
- `corpus/SOURCES.md:105` at HEAD `6631401`
- `corpus/README.md:212` at HEAD `6631401`
- `corpus/knowledge/iso-29147-and-30111-division-of-labour.md:1,9-14,19,42,47`
- `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:56,66`
