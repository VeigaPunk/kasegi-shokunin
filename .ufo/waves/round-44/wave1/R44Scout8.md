# R44Scout8 — public-source candidates vs chousa / kake / kengaku

Seat: scout, read-only. Item: check public-source candidates against sibling scope and report contested boundaries. No production edit, no commit, no tool install. Pacman not invoked. `RULES.md` read; nothing installed.

Pinned commits:

- kasegi freeze `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` is an ancestor of HEAD `66314015122b9aa32dc40f2f1815df56624c26d1` (`round-44: freeze claims and validated wave`). `corpus/README.md` blob is identical at both (`e3ee291c5f40234318691d23512cf0cd6f07f25b`).
- kake `1a48131577ba82c967650561be34e8dba909432a`
- chousa `9eef15e7c0e0ae0055228e7066dc1eec676a91d2`
- kengaku `30801b479e3418c11089b8586178b6960216f364`

LSP: no language server in this seat's tool list. Locations below are text matches, not semantic lookups.

## Candidate set

Committed unopened leads, `corpus/SOURCES.md` at the freeze (same lines at HEAD):

- `:104` Google Big Sleep reporting; DeepMind blog URL returned 404 in that pass; `https://goo.gle/bigsleep` was not opened.
- `:105` ISO/IEC 29147 and ISO/IEC 30111 catalog records, `https://www.iso.org/standard/72311.html` and `https://www.iso.org/standard/69725.html`.
- `:106` UK AISI report, `https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing`.

Uncommitted worktree rows, absent from freeze and from HEAD (`git grep S069` on both returned no registry/README hit). `git status --short` shows `M corpus/README.md`, `M corpus/SOURCES.md`, plus untracked `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`, `corpus/source-snapshots/round-44/`, `.ufo/waves/round-44/source-recon/`. This seat did not write them.

- Worktree `SOURCES.md` adds S069 `https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules` (mined) and S070 `https://bughunters.google.com/about/rules/about-this-section` (rejected).
- Worktree `README.md` appends an F26 row for that Cloud VRP page.

## Sibling URL sweep

Command (markdown only, three lane trees):

```
rg -l -g '*.md' -F <url> chousa-shokunin kake-shokunin kengaku-shokunin | wc -l
```

| URL | files |
|---|---|
| `aisi.gov.uk` | 0 |
| `goo.gle/bigsleep` | 0 |
| `iso.org/standard/72311` | 0 |
| `iso.org/standard/69725` | 0 |
| `bughunters.google.com` | 0 |
| `rfc-editor.org/rfc/rfc9116` | 3, all kake |

The three rfc9116 files: `kake-shokunin/corpus/SOURCES.md`, `corpus/lessons/round-35.md`, `corpus/lessons/round-35-verifier-spotcheck.md`. chousa and kengaku contribute none.

`securitytxt.org` hits are kake-only among the three (`corpus/SOURCES.md:87` S079, `corpus/knowledge/security-txt-publishing.md`, `PROVINCE.md:215`, `corpus/README.md:464`, `corpus/lessons/round-35.md:45`). At the kasegi freeze, `git grep securitytxt.org corpus` hits the round-38 lesson, `source-snapshots/round-38/S055.txt:475`, and `source-snapshots/round-40/S021.txt:359`. No kasegi registry row.

## Contested boundary — RFC 9116 (held by both registries)

Same normative URL:

- kasegi freeze `corpus/SOURCES.md:69` S063, scope cell: disclosure-channel discovery format a target publishes at `/.well-known/security.txt`. Frontier `corpus/README.md:563` F24, status admitted. Reader instruction in that row: read the channel from the file the target publishes. Entry `corpus/knowledge/rfc-9116-security-txt.md` quotes §2.5.3 Contact MUST (`:12`), §3 location MUST (`:29`), §2.5.5 Expires MUST (`:24`), §5.5 no implied permission (`:46`). The entry contains no `kake` token.
- kake HEAD `corpus/SOURCES.md:86` S078, same `https://www.rfc-editor.org/rfc/rfc9116.txt`. Scope cell: normative requirements for the security.txt a publisher serves (location, media type, Contact, Expires). Anchor quotes the same Contact MUST, Expires MUST, and `/.well-known/` placement. Entry `corpus/knowledge/security-txt-publishing.md:4` scopes the entry to serving one file from GitHub Pages; `:13` also states the researcher-facing purpose ("a researcher must find a reporting channel"); `:20-21` restates the well-known location; `:72` restates that publication grants no permission to test. The entry contains no `kasegi` token.

Round-41 search log (`corpus/SOURCES.md:100` at the freeze) limited its coverage grep to kasegi `corpus/`, `SKILL.md`, and existing captures. It records no sibling registry check.

The lane already filed the overlap and left it open:

- `SCORECARD.md:1617` — coverage held, not verified; `CritProvinceBoundary` found shared RFC 9116 ground with kake; no coverage-score increase pending an L0 ruling. `:1628` says revisit F24 only after that ruling. `:1630` round-42 correction leaves that standing unchanged.
- `LOG.md:1744` and `:1791` — F24 parked pending the round-41 L0 ruling.
- `SHONEN.md:230` — cross-domain box `[~]`; shared fields, scope, expiry, and non-authorization in kake's entry; ruling requested.
- Fleet `.ufo/l0-questions.md:189` — the question is still the last kasegi line in that file. Later lines are other lanes. No answer is recorded there.

Split already written in the two scope cells: kasegi S063 is the discovery format a reader uses; kake S078 is the file a publisher serves, and the kake entry adds the Pages/Jekyll build path (S080, S006, S086). The shared bytes are the RFC's field, location, expiry, and non-authorization sentences. A further public source that re-quotes those sentences from `rfc-editor.org/rfc/rfc9116.txt`, or that opens `https://securitytxt.org/` (kake S079), sits on this unresolved split.

## Boundaries checked and not a second holding

**security.txt `CSAF` label.** kake `security-txt-publishing.md:63` names `CSAF` as a securitytxt.org extension (S079). kasegi `corpus/lessons/round-38.md:79-83` already records that sentence as adjacent: no product-status vocabulary, no kake CSAF registry row, F21 stays on S055. Re-read of `:63` matches that record. No new contest.

**Three unopened leads.** Zero markdown hits in the three sibling trees. Inside kasegi, the ISO catalog URLs are a different document from F11 / S041: `corpus/README.md:212` and `corpus/SOURCES.md` S041 cite the JPCERT/CC 2026 guideline PDF and name the 2014 edition as what that guideline compares. The AISI URL is a different document from F04 (`corpus/README.md:205`, sources S009–S012). Big Sleep's lead line says the candidate page was not opened. chousa `PROVINCE.md:3-11` owns source-hierarchy method and refuses bounty-program scope and claim packages, handing those to kasegi; it has no row for these three URLs. kengaku `PROVINCE.md:3` is LLM/model evaluation and `:30` refuses kasegi bounty-ledger mission state; it has no row for these three URLs. Province sentences and empty registries are both on the record; this seat does not turn either into an admission or a rejection.

**Worktree Cloud VRP (S069) and rules directory (S070).** Zero sibling markdown hits for `bughunters.google.com`. kake S085 (`corpus/SOURCES.md:93`) is `https://www.google.com/.well-known/security.txt` and its scope cell says that file is not a statement about Google's vulnerability programme. Different URL from S069. chousa's refusal sentence and kengaku's ledger refusal do not add a second row.

**Census `W04`.** `scripts/sources-census.sh:33` and `:643-645`: W04 is one lane repeating a URL under a different scope cell. Freeze control `.ufo/waves/round-44/controls/do-nothing.txt:18-22` prints W04 for kasegi S028 and S029. Those are S006 vs S028 (same HackerOne URL, `corpus/SOURCES.md:12` and `:34`) and the CRA pair S024/S029. That warning is intra-registry. It is not a chousa/kake/kengaku collision.

## Do-nothing

At `5ab3a60` (README blob also at HEAD):

```
git show 5ab3a60:corpus/README.md | grep -cE '^\| F[0-9]+ \| admitted \|'          → 0
git show 5ab3a60:corpus/README.md | grep -cE '^\| F[0-9]+ \| .* \| admitted \|'    → 25
```

The first pattern is C2's counter in `.ufo/waves/round-44/claims.json`. The second is the freeze control in `do-nothing.txt:10`, which recorded 25. Admitted frontier rows in this file put the title between `Fnn` and `admitted` (`corpus/README.md:563`). The claims.json pattern does not match that shape, on the freeze or on the dirty worktree.

Worktree file only (uncommitted F26 append): the do-nothing pattern returns 26; the claims.json pattern still returns 0. A dirty tree is not the frozen base. This seat did not add the row. Reading sibling boundaries does not create F26, a knowledge file, or a registry row.

C1's eight routed defects were not re-counted here.

## Limitations

- Lead URLs were not fetched again. The Big Sleep lead already records that its first URL 404'd and that the tracker was not opened.
- Sibling sweep is markdown under the three lane checkouts. It does not cover other lanes (kaidoku's OSV row is outside this item).
- `HYAKU_SCRATCH` is unset in this process. No scratch directory was created, including under `/tmp`. Nothing to delete.
- Worktree S069/S070/F26 and `source-recon/` are observed only. They are not committed evidence and are not this seat's writes.
