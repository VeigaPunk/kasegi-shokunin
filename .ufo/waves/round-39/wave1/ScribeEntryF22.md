# ScribeEntryF22 — knowledge entry for F22 (CISA, When to Issue VEX Information)

Seat: scribe (leaf, no dispatch). Round 39, axes owned by the round: coverage (this seat's judged axis), depth:verifiability read-only. Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `480b1a505a2dfc14a4f718d16d63808247214d0a`. No mutating git, no lane writes outside this receipt and the one deliverable, no tool installs.

## Deliverable

- `wave1/ScribeEntryF22.entry.md` — the landable knowledge entry for `corpus/knowledge/cisa-when-to-issue-vex.md` (L1 lands it; this seat does not).
- 144 lines, 19,196 bytes, `sha256 5010a107cc7ef34bcd7e8d1a74eb2a2bb2a71c3ea666577506d7c2f93dc25d29` (first cut, before the harness-binding fix below: 18,998 bytes / `874ca53b…`).
- Every blockquote attribution carries the capture name (`— S057.txt:L12-L14`), so S057 is cited in the body, outside the `source:` and `recheck:` lines (23 body lines mention it).
- `cmp` of the landed file against the scratch draft: identical (scratch copy deleted after the copy, before this receipt).
- Landable bytes only: no validation table, no receipt scaffolding, no headings outside the entry text. All evidence lives here.

## Provenance trio (CORPUS)

1. Header `source: S057 — https://www.cisa.gov/resources-tools/resources/when-issue-vex-information — capture corpus/source-snapshots/round-39/S057.txt (275 lines, 17,971 bytes; sha256 11c8d6d6…)` with a per-section line anchor list (L1 title … L215-L227 open-source section).
2. Executable recheck in the entry, `cd`-prefixed, human note after `#`:
   `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057`
3. The manifest + capture pair it names (`corpus/source-snapshots/round-39/manifest.json`, `S057.txt`), landed by ExecFrontierCapture this wave.

### Source facts, re-fetched by this seat

```
$ date -u +%Y-%m-%dT%H:%M:%SZ; curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o vex.pdf \
    -w 'http=%{http_code} bytes=%{size_download} ct=%{content_type} url=%{url_effective}\n' \
    https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf
2026-10-26T19:31:07Z
http=200 bytes=235270 ct=application/pdf url=https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf
cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99  vex.pdf
```

The raw PDF digest and byte count equal the round-38 lead ledger and the landed manifest (`fetched_bytes=235270`, `fetched_utc=2026-10-26T19:30:55Z`). Normalizing with the instrument's own `pdf_to_text()` (`pdftotext -enc UTF-8` then whitespace collapse; imported read-only from `corpus/instruments/capture-source.py`) reproduced the capture byte for byte:

```
snapshot_bytes=17971 lines=275 sha256=11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f
$ cmp S057.txt .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt && echo CMP-IDENTICAL
CMP-IDENTICAL
```

### Capture-normalization conflict, resolved before filing

The frozen claims/round-39 anchors are `pdftotext -layout` line numbers (business decision L19-20 and L129, lifecycle+timestamp L205-213, inheritance L287-294); my `-layout` run gives 400 lines / 19,718 bytes / `sha256 d32b961ce530e97389e08db6e160bd98fa88db91f8620a1604ee50a81d5daa35`, which matches those anchors but is NOT the landed capture. ExecFrontierCapture landed the instrument-normalized (collapsed) bytes — 275 lines / 17,971 bytes / `sha256 11c8d6d6…` — and replied that the `-layout` numbering is out of range for a 275-line file (`source-recheck` would fail `anchor-out-of-range`). I rebound every citation in the entry to the collapsed numbering; the entry is internally consistent with the landed capture, and the `-layout` numbers appear nowhere in it. The map for the record: 13→19, 80→129, 133→206, 137→212, 184→286, 190→292.

## Harness binding (rule A/C), after ExecHarnessProbe's measurement

ExecHarnessProbe measured on a scratch mirror of base `480b1a5` + these artifacts that the harness counts an S-id as cited only when it appears outside the `source:` and `recheck:` lines (`selection-not-cited-by-entry` otherwise), that an evidence bullet beginning `- S054, …` is a DECLARATION (`header-sources-not-rechecked`), and that the `recheck:` comment is scanned for `--source` tokens. The first cut of this entry named S057 only in the header. Fixed by rebinding every blockquote attribution to the capture name (`— S057.txt:L…`, the F21 `(S055.txt:2135)` shape):

```
$ grep -c '^> ".* — S057\.txt:L' wave1/ScribeEntryF22.entry.md   → 22
$ body lines (excluding the source: and recheck: lines) containing S057 → 23
$ grep -nE '^- S[0-9]|--source'  → only the recheck: line's own --source S057 (no evidence-list bullet, no --source token in the comment)
```

Re-run of the quote checker after the rewrite (capture copied from the landed `wave1/ExecFrontierCapture.S057.txt`):

```
blockquote spans=22 distinct=22 words_max=25 anchors_ok=22 fails=0
body_S057_lines=23 first=20 last=117
```

The row-level harness run needs the landed entry plus the admitted SOURCES/README rows, which this seat may not write; ExecHarnessProbe ran it on an assembled tree (`git archive 480b1a5` + this entry as `corpus/knowledge/cisa-when-to-issue-vex.md` + the capture and manifest + `ScribeFrontierF22.readme.append.md`). Their measured result on these bytes:

```
unlanded cd prefix: FAIL F22 … ids=S057 exit=2 problems=recheck-exit-2 ; entries=25 pass=24 exit=1
  → every rule applied BEFORE exec passes on the entry text: one source: line, one recheck: line,
    one --source token, zero evidence-bullet declarations, 22 S057.txt: prose citations,
    manifest schema_version 1 with ids ['S057']
cd prefix repointed at the assembled tree (one line changed, nothing else):
  PASS     F22  knowledge/cisa-when-to-issue-vex.md  ids=S057  exit=0 ; entries=25 pass=25 exit=0
  exec: S057:sha256 OK ; Q1 anchor=12-ok ; Q2 anchor=132-ok ; Q3 anchor=136-ok ; Q4 anchor=184-ok
```

They also regenerated the capture independently with `capture-source.py pdf_to_text()`: byte-identical, `sha256 11c8d6d6…`, 275 lines, 17,971 bytes — the header digests agree with the landed bytes. Their conclusion matches mine: no entry change is needed; the remaining obligation is landing order — entry, `corpus/source-snapshots/round-39/S057.txt` and the manifest must land in one tree, or the landed row reads `recheck-exit-2`. Recorded on their side as §H of `wave1/ExecHarnessProbe.harness.txt`.

## Verification performed

**Quote binding (Q3/Q8/Q9, declared normalization = whitespace collapse).** A scratch checker normalized the capture to single spaces, mapped offsets back to capture lines, and required each quoted span to occur and to overlap its declared line range:

```
blockquote spans=22 distinct=22 words_max=25 anchors_ok=22 fails=0
inline spans=49 distinct=47 not-exactly-once=10 maxwords=20
  INLINE (2, 'may be different than VEX information from suppliers')   # cited at both lines L54-L55 and L61-L62
  INLINE (0, ...)                                                      # 9 counts are the rejected-claim headings, deliberately not source quotes
```

Every evidence quote is exactly-once under collapse except that one phrase, which carries both of its anchors; every blockquote is ≤25 words. After rebinding the last duplicate fragment the two "should be issued" occurrences were disambiguated by quoting `an “under_investigation” status should be issued` (unique).

**FC figures recomputed on the landed capture, not on a draft:**

```
VEX=101 KEV=1 EPSS=0 SSVC=0 CSAF=0 CVSS=0 inherit=4 action_statement=2 impact_statement=1
under_investigation=2 not_affected=3
component_not_present=1 vulnerable_code_not_present=1
vulnerable_code_not_in_execute_path=0 vulnerable_code_cannot_be_controlled_by_adversary=0 inline_mitigations_already_exist=0
$ grep -n "under_investigation"  → 111, 133
$ grep -n "business decision"    → 13, 80
$ grep -n "could be inherited downstream" → 190
```

**Recheck line: syntax, fail-closed, and pass path.**

```
$ bash -n <<<"$line"   → bash-n=OK
$ ( cd /tmp && bash -c "$line" )      # manifest not yet landed in the lane
manifest UNAVAILABLE reason=missing
exit=2
$ python3 corpus/instruments/source-recheck.py --manifest "$PWD/trio/manifest.json" --source S057   # wave1 manifest + capture copy
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
trio_exit=0
```

So the trio passes on the bytes that will land, and the line fails closed (exit 2) from a foreign cwd while the manifest is absent — the Q7 missing-source control.

## QUALITY conformance (Q1–Q10) as drafted

| id | how the entry satisfies it |
|---|---|
| Q1 | H1, then `source:` (S057, URL, capture path, 275 lines/17,971 bytes/sha256, per-section anchors), `verified-at:` (2026-10-26 + fetch facts), `ground: F22`, `recheck:` (runnable, fail-closed). |
| Q2 | Sole support is S057, tier A, mined this round; every claim's quote is on a line of that capture. |
| Q3 | 22 blockquoted spans, all ≤25 words, all verbatim under declared collapse, each with its line; 49 shorter inline quotes cited by line. Numbers (`275`, `17,971`, `235,270`, digests) are copied from the file and the fetch, not retyped. |
| Q4 | CISA's own guidance, stated as CISA's ("CISA guidance, not a standard"); no vendor practice asserted — the entry says explicitly that the document makes no claim that any named supplier publishes VEX. |
| Q5 | Falsifiable rule with six failure conditions (a)–(f), FC-1…FC-6, and eight rejected over-generalizations each with its reason. |
| Q6 | Documentation only: no probing/scanning/submitting instruction, no credential, session, private URL or vault URI. |
| Q7 | The recheck is a command, its pass output names the pinned capture (`S057:sha256 OK`, `Q<n> OK anchor=…-ok`), and the missing-source control exits 2 (shown above). |
| Q8 | Normalization declared: whitespace collapse; `<u>` markup is not present in this PDF capture, so FC-1's statement is exact for these bytes. |
| Q9 | Quotes are exactly-once or carry their anchor; the one repeated phrase is cited at both of its lines. |
| Q10 | One command, `bash -n`-parseable, `cd`-prefixed to the lane root, note after `#`. |

## Coverage contribution (why this entry, for the L1)

- Provides the `source: S057` declaration, the `--source S057` recheck, and body citations (`— S057.txt:L…`) that the harness binds (rule A both directions; the entry declares exactly `{S057}`, and the manifest lists S057). Prose references to S055/S053/S054/S052 are not declarations: no second `source:` line, no `- S0xx` evidence bullet (`grep -nE '^- S[0-9]|^source:'` returns line 3 only).
- Carries the layer distinction the round claims rest on: F22 is issuance/lifecycle/reaffirmation/inheritance policy; the field-level contract stays with F21/S055, and EPSS/SSVC/KEV stay with S053/S054/S052 — measured absent here (`EPSS=0 SSVC=0 CSAF=0 CVSS=0`, `KEV=1`).
- Counts toward `knowledge 50 → 51` and the `grep -rlE '^source: S057' corpus/knowledge | wc -l → 1` check once landed at `corpus/knowledge/cisa-when-to-issue-vex.md`.

## Not done here (by scope)

- No commit, no landing: the L1 places the entry at `corpus/knowledge/cisa-when-to-issue-vex.md`, the capture/manifest at `corpus/source-snapshots/round-39/`, and the SOURCES/frontier rows (ScribeRowS057 writes the row; ScribeFrontierF22 the frontier row).
- `frontier-recheck-count.py` was not run: it needs the landed entry plus the admitted rows in `corpus/SOURCES.md`/`corpus/README.md`, which this seat may not write. Its rules were checked against the drafted bytes instead (declaration shape, single `--source`, manifest exists and lists S057 — proven with the wave1 manifest copy above).
- The junk twin (`c2-controls/junk-f22.md`) rejection is ExecJunkRecheck's item; nothing here depends on its verdict.

## Tools

None installed, none upgraded (no pacman, no uv/npx). Tools used: `curl`, `pdftotext` (poppler 26.08.0), `python3`, `cmp`, `sha256sum`, read-only imports of `corpus/instruments/capture-source.py` and `corpus/instruments/source-recheck.py`.

## Scratch

`S=/fast/scratch/hyaku/kasegi-r39/ScribeEntryF22/` — created, used for the PDF, both normalizations, the quote checker and the trio proof, then removed after the deliverable copy (`rm -rf -- "$S"`); verified absent at filing.
