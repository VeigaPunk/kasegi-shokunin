# ReviewC2 — adversarial review of the C2 draft entry (F56, S114)

Draft reviewed: `.ufo/waves/round-80/w1-input/osv-ubuntu-binary-to-source-mapping.md`
Against: `corpus/QUALITY.md` (knowledge-entry rows incl. R37, R56, R76, R108, R114, R121–R126, R131), `corpus/source-snapshots/round-80/S114.txt`, `corpus/source-snapshots/round-80/manifest.json`, frozen claims `.ufo/waves/round-80/claims.json` (B0–B7), control `.ufo/waves/round-80/controls/c2-prerecheck-r80.txt`.

## Verified clean (evidence)

- **Header trio present.** `source:` (S114 + capture path), `verified-at: 2026-11-06`, `recheck:` all present. R12 satisfied: `--source S114` covers the header's `source:` id.
- **`recheck:` is byte-exact B0.** claims.json `B0` command = `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-80/manifest.json --source S114`; the draft's `recheck:` value behind `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` is that exact string. B5's textual limb holds. Ran it (TMPDIR=scratch): prints `S114:sha256 OK` + six `S114:<pin> OK occurrences=1 anchor=<n>-ok` lines, `rc=0` — identical shape to `controls/c2-prerecheck-r80.txt`.
- **All six quotes verbatim at their cited lines** (numbered `nl -ba` over the committed capture): Q01→25, Q02→35, Q03→35, Q04→38, Q05→39, Q07→58, each a character-exact substring; each `occurrences=1`. Free anchors also checked against the numbered capture: heading `:22-23` ✓, experimental paragraph `:33` ✓, payload skeleton `:41-46` ✓, request sample + example response `:48-72` ✓, results-array shape `:60-71` ✓ (objects at 61-65/66-70 carry only `source_names`), unpinned ordering clause quoted in "Not claimed" is the verbatim leading clause of `:58` ✓.
- **Word counts (R56):** re-measured with `wc -w`: 11 / 16 / 14 / 9 / 12 / 20 — all six match the Gate table.
- **Capture identity:** `sha256sum` = `e1ccfb9bd13bb3f9a077feb60ae5d738ccb47bc85f630aef9a7a5776ca8788d2`, `wc -c -l` = 2365 bytes / 73 lines — match manifest; manifest records `final_url` == requested URL, `fetched_utc 2026-11-06T19:42:42Z`, raw 18769 bytes. Gate section's provenance sentences all grounded.
- **All five Limits greps reproduce** (run from lane root, exit codes mine):
  - `grep -n -i -E 'rate limit|ratelimit|quota|api key|api_key|authenticat|credential' corpus/source-snapshots/round-80/S114.txt` → no output, `rc=1`
  - `'paginat|page_token|next_page_token'` → no output, `rc=1`
  - `'error|status code|throttl|400'` → no output, `rc=1`
  - `'severity|CVE|cvss'` → no output, `rc=1`
  - `'Debian|deb|dpkg'` → no output, `rc=1`
- **Subject sweep reproduces:** `grep -rli 'ubuntu' corpus/knowledge/` → no output, `rc=1` (93 entries present: `ls corpus/knowledge/*.md | wc -l` = 93, matching B2's "93 → 94" start). Literal sweep claim matches the control (`zero 6 of 6 knowledge files 93`).
- **Distinctness file:line cites open and carry their tokens** except finding 3 below: `osv-post-v1-query-contract.md:75` holds "…and the experimental endpoints, S108.txt:5-9). They are listed, not described." ✓; `osv-post-batch-query-contract.md:37` holds the 1,000/3,000 vulnerabilities counts ✓ (F55 `osv-determineversion-cc-library-versioning.md` exists, and "turns C/C++ file hashes into a library version" matches its pinned S113.txt:25 purpose quote).
- **No restatement of F51/F54/F55/F31 ground.** The six claims are the binary-to-source page's own clauses; the ordering clause is explicitly not claimed; none of the six quotes occurs in any admitted entry (control literal sweep 0/6).
- **[INFERENCE] marks are where needed:** Claim 3's separate-call reading and Claim 4's rejection-behaviour gap are both marked; every rejected over-generalization is anchored to the line that refuses it.

## Findings

### F-1 (Major, R37 + R108 framing) — unreceipted run-result sentence, contradicting the entry's own attribution frame

Attribution says "Every statement below is that page's own declared behaviour, quoted from the pinned capture…", and the next sentence states a live-probe result that is not page behaviour and is committed nowhere: "the experimental-path form of the URL (`.../post-v1experimental-ubuntu-binary-to-source/`) answered HTTP 404 on 2026-11-06". No committed transcript carries that probe (absent from `.ufo/waves/round-80/controls/`, from both round-79 lessons), and the sentence carries no `report-only` mark — R37: a lane record that quotes a run result carries a committed transcript, or the quoting sentence says `report-only`. The claim is true (the frozen claims.json motivation records the same 404) but as written the entry is self-contradicting and unverifiable from committed bytes.

Exact fix — replace the two sentences:

> The page sits at `https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/`; the experimental-path form of the URL (`.../post-v1experimental-ubuntu-binary-to-source/`) answered HTTP 404 on 2026-11-06, so the round-79 lead's path name is not the page's address.

with:

> The page sits at `https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/`, the URL the manifest records as both the requested and the final URL at HTTP 200 (`corpus/source-snapshots/round-80/manifest.json`, `fetched_utc 2026-11-06T19:42:42Z`). The experimental-path form of the URL (`.../post-v1experimental-ubuntu-binary-to-source/`) answered HTTP 404 in this entry's own probe of 2026-11-06, report-only, no transcript committed; the pinned capture, not that probe, is the ground, and it is why the round-79 lead's path name is not the page's address.

and change "Every statement below is that page's own declared behaviour" to "Every claim below is that page's own declared behaviour" (so the report-only probe sits outside "every claim").

### F-2 (Minor, R114) — subject sweep omits the registry leg and the per-hit verdict

The Distinctness sweep is `grep -rli 'ubuntu' corpus/knowledge/` only. R114's check runs the subject over `corpus/SOURCES.md` **and** `corpus/knowledge/*.md`, with a per-hit verdict. The registry does hit once: `grep -n -i 'ubuntu' corpus/SOURCES.md` = line 126 only — the S114 row this very entry admits. The recorded sweep must show that hit and its verdict, or the distinctness record is incomplete by R114's letter.

Exact fix — append to the subject-sweep bullet:

> Registry leg of the same sweep: `grep -n -i 'ubuntu' corpus/SOURCES.md` prints one hit, `:126` — the S114 row this entry admits (per-hit verdict: this entry's own source row, not another holder of the subject); no other registry row carries the subject.

### F-3 (Minor, R131) — F54 ordering cite names the heading, not the sentence

Distinctness cites `corpus/knowledge/osv-post-batch-query-contract.md:19` for the input-matched ordering guarantee. `:19` is the heading `## Claim 2 — the response ordering is guaranteed to match the input`; the quoted ground sentence "The response ordering will be guaranteed to match the input." (S112.txt:24) sits at `:21` (`grep -n 'guaranteed'` → 19, 21, 73). R131's precedent (M80-2) is cite-the-line-that-holds-the-token.

Exact fix — in the F54 bullet, change `osv-post-batch-query-contract.md:19` to `osv-post-batch-query-contract.md:21`.

### F-4 (Minor, R108-adjacent) — F31 characterized more broadly than its ground

Distinctness says F31 "holds the OSV record format". F31's own title scopes it to "the OSV format's per-package version timeline: `affected[].ranges[].events` …" — the affected-range portion, not the record format at large. The contrast drawn (the binary-to-source response is not an OSV record) survives the narrower wording.

Exact fix — change "holds the OSV record format" to "holds the OSV record's affected-range events format".

### F-5 (Minor, records completeness) — the frozen control's paraphrase pre-sweep prints a bare `1` with no per-hit disposition

`controls/c2-prerecheck-r80.txt` ends: `# R125 paraphrase pre-sweep (L1): keyword hits in admitted entries` / `1`. One keyword hit in an admitted entry is recorded with no hit named and no verdict. R114 requires a per-hit verdict; B6 requires the paraphrase sweep to record each clause novel and no restatement. The control bytes are frozen and not mine to change; the disposition belongs in the landed record.

Exact fix — the L1 adds one sentence to the entry's Distinctness section at landing (naming the actual hit the sweep found):

> The R125 paraphrase pre-sweep (`controls/c2-prerecheck-r80.txt`, final line) recorded one keyword hit in an admitted entry: `<file:line>`, `<keyword>` — verdict: `<why it is not one of the six clauses>`, so the pre-sweep finds no restatement.

### F-6 (Nit, optional) — Claim 6's rule leans on the unpinned leading clause of the same line

The falsifiable rule's second limb ("drops empty objects and then pairs the remaining results with its input names") presupposes positional pairing, which line 58 states only in its unpinned leading clause. The dependence is already disclosed in "Not claimed", so this is cosmetic. Exact fix — append to the rule: "(the pairing is the ordering clause `:58` opens with — unpinned; the rule describes a misreading of the pinned clause, not a claim of the ordering)."

## Residual risk / gaps

- The 404 probe (F-1) is re-runnable but will rot; after the fix it is honestly report-only.
- The five Limits greps and both sweeps are live-tree commands; the R125 keyword-hit disposition (F-5) is the only piece whose input I could not re-derive from committed bytes.
- Frozen bytes untouched throughout; every command ran read-only over committed bytes from the lane root (scratch `/fast/scratch/hyaku/kasegi-r80/ReviewC2`, removed at exit). No tool installs were needed.

## Verdict

All findings are prose-level fixes the L1 can apply before landing; none touches the six frozen quotes, the manifest, the snapshot, claims.json, or any B0–B7 limb.

C2-REVIEW = no-blocker
