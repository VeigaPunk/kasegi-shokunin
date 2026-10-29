# Round 46 (attempt 2) — `## Gate` block DRAFT for S074 / F29

DRAFT by seat `R46bScribeLesson` for the L1's append to `corpus/lessons/round-46.md`
(section `## Attempt 2 (2026-10-29, L1 KasegiR46)`). All quoted outputs below are runs this seat
performed; nothing here is committed.

---

## Gate — frontier F29, source S074, and rejection

### Source

- **URL:** `https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories`
  (the canonical URL; `capture_url` equals it; HTTP 200, `final_url` equals the row URL).
- **Access date:** `2026-10-29` (manifest `fetched_utc` `2026-10-29T20:19:30Z`; `verified-at: 2026-10-29`).
- **Capture:** `corpus/source-snapshots/round-46-a2/S074.txt` — sha256
  `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, 42 lines, 7087 bytes.
  Manifest: `corpus/source-snapshots/round-46-a2/manifest.json` (sha256
  `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`) — a NEW manifest beside the
  attempt-1 one, which stays byte-identical (its sha256 `01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34`
  is pinned by the attempt-1 receipts).
- **Recheck (the entry's `recheck:` line, exact form required by the gate's H2 limb):**

  ```
  recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074
  ```

  Run by this seat against the frozen capture and manifest:

  ```
  S074:sha256 OK
  S074:Q1 OK occurrences=1 anchor=10-ok
  S074:Q2 OK occurrences=1 anchor=13-ok
  S074:Q3 OK occurrences=1 anchor=17-ok
  S074:Q4 OK occurrences=1 anchor=24-ok
  S074:Q5 OK occurrences=1 anchor=25-ok
  S074:Q6 OK occurrences=1 anchor=25-ok
  S074:Q7 OK occurrences=1 anchor=26-ok
  S074:Q8 OK occurrences=1 anchor=31-ok
  S074:Q9 OK occurrences=1 anchor=38-ok
  RC=0
  ```

### Located quotes (nine, one per frozen core; each ≤ 25 words, each located on its anchor line)

Each quote below was verified twice: (i) `sed -n '<anchor>p' corpus/source-snapshots/round-46-a2/S074.txt`
prints a line that contains the quote text, and (ii) a substring check of the quote inside that anchor
line returns `substring=True` (the run output is in `evidence.md`). Word counts are the quote's own.

| id | anchor | words | frozen core it carries | quote |
|---|---|---|---|---|
| Q1 | `S074.txt:10` | 19 | **core 1** — "privately discuss and fix a security vulnerability" | “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” |
| Q2 | `S074.txt:13` | 11 | **core 2** — "temporary private fork" | “Privately collaborate to fix the vulnerability in a temporary private fork.” |
| Q3 | `S074.txt:17` | 12 | (credit) | “You can give credit to individuals who contributed to a security advisory.” |
| Q4 | `S074.txt:24` | 15 | **core 3** — "authorized to assign CVE identification numbers" | “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” |
| Q5 | `S074.txt:25` | 8 | **core 4** — "reviews the request within 72 hours" | “GitHub usually reviews the request within 72 hours.” |
| Q6 | `S074.txt:25` | 11 | (the request does not publish) | “Requesting a CVE identification number doesn't make your security advisory public.” |
| Q7 | `S074.txt:26` | 14 | (the other-CNA bar) | “GitHub cannot assign CVEs to your project if it is covered by another CNA.” |
| Q8 | `S074.txt:31` | 22 | (publication visibility) | “Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.” |
| Q9 | `S074.txt:38` | 15 | **core 5** — "add a fix version to a security advisory prior to publishing" | “you should add a fix version to a security advisory prior to publishing the advisory” |

Core coverage, computed over the manifest's own quote records (the gate's H4 rule): all five frozen cores
are inside the quoted text — `privately discuss and fix a security vulnerability → Q1@10`,
`temporary private fork → Q2@13`, `authorized to assign CVE identification numbers → Q4@24`,
`reviews the request within 72 hours → Q5@25`,
`add a fix version to a security advisory prior to publishing → Q9@38`; 9 quotes, 9 distinct texts,
8 distinct anchors (the gate requires ≥7 distinct anchors and pairwise-distinct texts).

### Admit row

**Frontier row F29** (appended to `corpus/README.md`; the frontier table is appended, never edited in
place). Draft row for the L1 to land:

```
| F29 | GitHub repository security advisories, maintainer flow: private discussion and fix of a vulnerability, the temporary private fork, advisory credit, the CVE identification number requested from GitHub as a CNA (72-hour review; no CVE where another CNA covers the project), publication, and the fix-version duty before publishing | admitted | `corpus/knowledge/github-repository-security-advisories.md` | S074 | Keep the maintainer-side advisory lifecycle distinct from the reporter-side private reporting flow (F28) and from the CVE Program's own CNA assignment rules (F07); re-open the GitHub Docs page before relying on its 72-hour review or its fix-version wording. The public GitHub Advisory Database is outside F29. |
```

**SOURCES row S074** (appended to the `## Registry` table of `corpus/SOURCES.md`; 11 cells, kind `docs`,
tier `A`, status `mined`, opened `2026-10-29`, recheck `180d`):

```
| S074 | GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories | docs | A | GitHub's own statement of the maintainer-side repository security advisory lifecycle: the private discussion and fix of a vulnerability, the temporary private fork, credit, the CVE request through GitHub as a CNA, publication and the fix-version duty | lines 10-42 of corpus/source-snapshots/round-46-a2/S074.txt (heading L10, private-fork step L13, credit L17, CVE request L24-L26, advisory visibility L31, fix-version duty L38), sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039 (snapshot 42 lines, 7087 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL) | Draft the advisory privately, request the CVE while it is still private, and set the fix version before publishing: a published advisory without a fixed version leaves Dependabot alerting users with no safe version to update to. | mined | 2026-10-29 | 180d | corpus/knowledge/github-repository-security-advisories.md |
```

**Evidence for the two rows** — the admission gate `corpus/instruments/r46-f29-gate.py` was run by this
seat on a scratch export of the freeze commit (`fe0f56b7`) into which the two draft rows above were
inserted (plus a stub entry file, because the gate's H3 limb requires the `used-by` entry to exist):

```
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=0 read=source=0 verified-at=0 recheck=0 sections=0/4 full=0/4 table-rows=0 xrefs=0/0 anchored=0
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate H6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=0 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=4/7 exit=1
```

The three red limbs are the entry's own work (H2/H5 need the real entry's shape and located spans; H6
needs the real entry's bytes, not the stub) and are the L1's integration surface, not the rows'.

Do-nothing controls on the same freeze export: without either draft row the gate reads
`gate H1 pass=0 read=rows=28 admitted=28 dup=0` and
`gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0`
(`f29-gate fixed=2/7 exit=1`); with the S074 row present but the entry file absent, H3 reads
`bad=used-by` and the census reads `file	E11	S074 missing used-by corpus/knowledge/github-repository-security-advisories.md`
(exit 1, so H7 reads `census-rc=1 ok-line=0`). The rows and the entry therefore have to land together —
see `status-recheck-usedby.md` §"The row and the entry must land together".

### Rejected / flipped candidates

The attempt-2 claims file carries no `candidates` key (`claims.json` top-level keys are `schema`, `lane`,
`round`, `attempt`, `author`, `base`, `note`, `claims`, `sourced_claim`, `frontier_step`; the string
"candidate" does not occur in it), so the candidate list below is reconstructed from the lane's own
corpus evidence and the attempt-1 `## Gate` section of `corpus/lessons/round-46.md`. This is a stated
deviation from the seat brief, not a silent substitution.

1. **F29 = GitHub private vulnerability reporting (the reporter-side flow) again — REJECTED.**
   *Reason:* that ground is already admitted as **F28** (`corpus/README.md:666`, source `S073`, entry
   `corpus/knowledge/github-private-vulnerability-reporting.md`); S073's own scope cell reads "GitHub's
   own statement of the reporter-side private-reporting flow only (who may report, the form's default
   fields, submission and the temporary private fork); **not maintainer handling of a report, the GitHub
   Advisory Database or CVE assignment**", i.e. the reporter side and the maintainer side are two
   grounds, and only the maintainer side is new. Re-admitting it would also breach C2's kill rule
   ("the frontier row's sources cell names any source other than S074 for the same ground
   (double-counting)").
   *Flip condition:* F28 is withdrawn from the frontier table and its entry removed, or S073's scope is
   re-written to cover the maintainer side — then the reporter-side flow may be re-admitted as a row
   against S073 and this row is void.
2. **The public GitHub Advisory Database as the source for the same ground — REJECTED.**
   *Reason:* the database is a record republication, not the maintainer lifecycle; the lane already
   screened it once and refused it — row **S068** (`corpus/SOURCES.md:74`, status `rejected`, tier B)
   reads "REJECTED: screened out on primary-of-record and record completeness — the page republishes
   NVD's record of the CVE, self-labelled Unreviewed … with no package listed …, so it carries neither
   the …". F28's frontier row also states in its `next` cell that "Maintainer handling, the GitHub
   Security Advisory database and CVE assignment are outside F28" — the database is explicitly not part
   of this ground.
   *Flip condition:* a first-party GitHub page that documents the **advisory lifecycle itself** (not one
   advisory's record) is captured with its own manifest record and digest, and that capture — not
   `github.com/advisories/…` — becomes the row's source.
3. **CVE assignment / GitHub-as-CNA as its own frontier row from S074 — REJECTED.**
   *Reason:* the ground is already admitted as **F07** (`corpus/README.md:208`, source `S031`, entry
   `knowledge/cna-assignment-and-vulnerability-rules.md`, "CVE CNA operational rules"); the attempt-2
   claim's own `after` text says the new entry must carry "the F28/F07 contrasts", i.e. F29 crosses
   references the CNA rules rather than re-admitting them. S074's two CVE sentences are about **GitHub's
   own service behaviour** (a request, a 72-hour review, a bar where another CNA covers the project),
   which is the maintainer-side workflow, not the CVE Program's assignment rules.
   *Flip condition:* F07's entry is withdrawn, or S074 states an assignment rule that S031's capture
   does not hold — then a separate row may be written against S074.

**Carried, not a row:** the attempt-1 routed item, the `considerthese` ledger dispositions append
(`corpus/knowledge/considerthese-proposals-ledger.md`). It is not a frontier candidate and it is not part
of C2's surface; the attempt-2 gate's H6 limb exempts that ledger by name and minimum size
(`LEDGER_MIN_BYTES = 30696`) so an append does not couple with this claim, but the append itself lands
only when the L1 decides it (claims `frontier_step`: "lands this round together with the
`r46-c2-gate.py` ledger-exemption amendment if the wave verifies it, else the deferral is carried").
The attempt-2 errata file (`.ufo/waves/round-46/attempt2/counter-errata.md` §E3) records that amendment as
**CONDITIONAL** — it lands only if the wave's own verification succeeds, otherwise E3 is struck and the
append is deferred again with the reason. `r46-c2-gate.py` is otherwise frozen and unamended by the
wave's seats, so the deferral is the default outcome.

<!-- END OF (b) DRAFT -->
