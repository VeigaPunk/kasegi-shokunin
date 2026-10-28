VERDICT: DRAFT-READY

Scope: C1/R1 and C2 registry rows only (drafter B, independent). Draft file: `.ufo/waves/round-45/wave1/R45ScribeRowsB.draft/rows.md` (two table rows plus a short rationale paragraph). Nothing was committed, staged or edited in any tracked file; no git mutation; no tool installed or upgraded. Scratch root `/fast/scratch/hyaku/kasegi-r45/R45ScribeRowsB/` is removed at exit.

## Finding 1 — the two rows are well-formed (11 cells, NF=13, no pipe inside a cell)

Attacked: the draft rows S071 (Linux kernel security-bugs) and S072 (Google Bug Hunters Rules directory, article-API capture).

Command:
```
awk -F'|' '/^\| S07/ {print NR": NF="NF}' .ufo/waves/round-45/wave1/R45ScribeRowsB.draft/rows.md
```
Printed:
```
1: NF=13
2: NF=13
```
Contract-census malformed-row check on the candidate registry (`fx/cand/corpus/SOURCES.md`, base 70 rows + the 2 draft rows = 72 rows):
```
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
```
Printed: `0`. Duplicate-id check (`... | sort | uniq -d`) printed nothing. Row count `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` printed `72`.

## Finding 2 — the S072 teaches cell meets the seat spec and the contract

Command:
```
awk -F'|' '/^\| S072/ {t=$8; print (t ~ /readable/ ? "readable:yes" : "readable:NO"), (t ~ /^ *supersedes S070 — /  ? "opener:yes":"opener:NO"), (t ~ /flip:/ ? "flip:yes":"flip:NO")}' rows.md
```
Printed: `readable:yes opener:yes flip:yes`.

The cell opens `supersedes S070 — `, states that the body is readable through the article API (10029 characters), names the table structure, restates the S069 Q5 Cloud VRP line, and carries `REJECTED: …; flip: a fresh capture of the article-API body states a program-specific scope or boundary rule that the program's linked rules page does not state`. I kept the `REJECTED:` prefix even though the seat spec called it optional, because the contract (`CORPUS.md` §SOURCES.md, Shape: "Rejected rows read `REJECTED: <reason>; flip: <what would change the verdict>`") requires it.

## Finding 3 — every anchor value I cite was re-checked against the pinned capture bytes

Commands and printed output:

- `sha256sum corpus/source-snapshots/round-45/S071.txt corpus/source-snapshots/round-45/S072.txt` printed `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40` and `364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025`, both matching the sha values in the seat spec and in `manifest.json`.
- `wc -c -l` printed `20152 372` for S071 and `10032 312` for S072 (sizes/lines as cited).
- Heading locations in S071 (awk over underline lines, heading line = underline-line − 1): `3: Security bugs`, `10: Preparing your report`, `73: What qualifies as a security bug`, `109: Identifying contacts`, `174: Responsible use of AI to find bugs`, `254: Sending the report`, `299: Disclosure and embargoed information`, `329: Coordination with other groups`, `359: CVE assignment`, `368: Non-disclosure agreements`. The row's anchor cites these line numbers.
- S071 teaches grounding: `sed -n 95,96p` shows the AI rule (`**If you resorted to AI assistance to identify a bug, you must treat it as` / `public**`); line 310 shows `for up to 7 calendar days from the start` with the 14-day exception on line 311.
- S071 manifest quote Q4 (`anchor 41`): the sentence wraps — `By` ends line 41 and `definition if an issue cannot be reproduced …` is line 42; the manifest's start-line anchor is consistent with that.
- S072: `python3` check printed `S072 bytes 10032 chars 10030 lines 312`; JSON body length `10029`; `body == file[:-1]` is `True`. So the 10029-character figure is the article-API body, and the 10032-byte capture is that body plus one trailing newline with one curly apostrophe (3 bytes). The 10029-character count in the teaches cell is therefore correct as the body length.
- S072 section and row lines: `## Android & Friends` L17, `## Chrome & Friends` L57, `## Google & Friends` L107, `## Open Source` L171, `## Other` L249; the Cloud VRP row L146–L149 with scope text on L148–L149 (`Security issues affecting any Google Cloud product or web service that` / `handles reasonably sensitive user data`). S069's round-44 capture has the same sentence on L9–L11 (`In principle, any Google Cloud product … handles reasonably sensitive user data is intended to be in scope.`), so the "restates S069 Q5" claim holds.

## Finding 4 — census validation with the do-nothing control, the candidate, a path-satisfied stub and a malformed mutant

Fixtures are full copies of the pure base export (`/fast/scratch/hyaku/kasegi-r45/L1/pure`, verified `cmp`-equal to `git show dc5bb8c…:corpus/SOURCES.md` and to the lane working tree). Candidate = base registry with the two rows inserted after the S070 row (lines 77–78). Stub = candidate plus a one-line validator-only file at `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` (not a knowledge entry; used only to test that the sole finding is the path). Mutant = candidate with ` x|y` appended to S072's teaches (12 cells).

Command (same for each fixture, `<FX>` = fixture root, `--today` pinned so E08 is deterministic):
```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <FX>/corpus/SOURCES.md --today 2026-10-28
```

**(a) do-nothing control — base registry, exit 0:**
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScribeRowsB/tree/corpus/SOURCES.md
```
(The two W04 lines are pre-existing warnings; W-codes never change status.)

**(b) candidate — draft rows inserted, exit 1:**
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E11	S071 missing used-by corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
```
This is the expected single finding: the used-by entry lands with C2's knowledge entry, not in this seat. It is a missing-path error (E11), not a malformed-row (E01), duplicate-id (E03) or enum (E05–E07) error. S072's used-by is `—`, so it is not path-checked.

**(c) stub — path present, exit 0:**
```
file	W04	S028 duplicate url … across scopes
file	W04	S029 duplicate url … across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScribeRowsB/fx/stub/corpus/SOURCES.md
```
This shows the only candidate finding is the not-yet-landed path.

**(d) mutant — extra pipe in S072 teaches, exit 1:**
```
file	E01	S072 fields=12
file	E11	S071 missing used-by corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
```
The validator discriminates: a malformed row is caught as E01 with the right field count.

Census (`… census --file <FX>/corpus/SOURCES.md`, candidate, exit 0) printed `FLEET rows 72`, `FLEET tier.A 64`, `FLEET tier.B 5`, `FLEET tier.C 3`, `FLEET tier.invalid 0`, `FLEET status.queued 0`, `FLEET status.mined 57`, `FLEET status.rejected 15`, `FLEET status.invalid 0`, `FLEET missing 0`. Base census (`… census --file <tree>/corpus/SOURCES.md`, exit 0) printed `FLEET rows 70`, `FLEET tier.A 63`, `FLEET tier.B 4`, `FLEET tier.C 3`, `FLEET status.mined 56`, `FLEET status.rejected 14`, `FLEET missing 0`. The delta is exactly the two draft rows: S071 adds one tier-A mined row and S072 adds one tier-B rejected row.

**Process note (honest):** my first candidate run used a fixture containing only `corpus/SOURCES.md`, so ~70 spurious E11 lines (every existing mined row's used-by) appeared. Those lines are a fixture artifact, not a registry finding. I discarded that output, rebuilt the fixtures as full tree copies, and re-ran everything; only the outputs quoted above are cited.

## Finding 5 — tier and status decisions

- S071 tier **A**, kind `docs`, scope limited to the kernel security team's own intake/embargo rules (not the kernel's general development process). Justification: the page is the security team's own published process, pinned by sha256 to its RST source.
- S072 tier **B**, not A: it is a Google page, but its program-scope column paraphrases the operative rules on each linked program page (for Cloud VRP, S069 is the operative capture). Secondary for scope. Tier C was considered; B is kept because the row is a genuine overview, not a lead.
- S072 status `rejected`, `recheck 180d`, `used-by —`; the correction to S070 is a new row, per contract rule 2 (append-only), and S070 is left unchanged.
- No E04 risk: S070's URL (`bughunters.google.com/about/rules/about-this-section`) differs from S072's (`bughunters.google.com/rest/v1/articles/about/rules/about-this-section`), and the teaches opens `supersedes S070 — `.

## Limitations

- Drafted from the pinned captures and the frozen manifest; I did not re-fetch the live URLs (the spec's `fetched` timestamps are taken from `manifest.json` and `S071.headers.txt`, not re-observed here).
- The S071 teaches benefit is grounded in two quoted places (L95–L96 and L310–L311). Other S071 claims in the knowledge entry are outside this seat.
- The `used-by` path for S071 does not exist yet; the E11 line is expected and resolves when the knowledge entry lands. I did not create that entry (not my deliverable, and creating it would be fabrication from my side).
- `REJECTED:` prefix included (contract-required) although the seat spec called it optional.
- I ran no frozen C1/C2 counter (`r45-routed-defects.py`, `r45-c2-gate.py`, `r44-frontier-count.py`) — outside this seat's assignment.
- Tab characters in the quoted output are shown as the literal tab the validator printed; `\t` in my prose is not a literal backslash.

Tooling: none installed, upgraded or removed on this seat.
