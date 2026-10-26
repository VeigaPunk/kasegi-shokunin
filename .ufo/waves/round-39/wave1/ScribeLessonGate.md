# ScribeLessonGate — round-39 lesson `## Gate` inputs

Seat: scribe (leaf). Item: draft the round-39 lesson `## Gate` section — admitted F22/S057 with
quote block Q1-Q4, the three rejected rows with reason + flip, candidates considered and not
taken, the standing assimilation refusals carried, and the spot-check readiness pointer.
Deliverable only; no L1 landing, no product edits.

- Deliverable: `.ufo/waves/round-39/wave1/ScribeLessonGate.gate.md`
- Lines / bytes: **39 lines, 8,563 bytes**
- sha256: `0093dc7bd75315b60889db5ded9ffdff6056eb86a8ea22188ef069d6942b5145`
- Shape: one `## Gate` section, five subsections (`### Admitted …`, `### Rejected …`,
  `### Candidates considered and not taken`, `### Assimilation …`,
  `### Spot-check readiness …`). No validation tables, notes or headings outside the landed
  text; all evidence is in this receipt.

Current bytes (revision 3) carry three corrections over the first draft: the spot-check subsection
points at `wave1/ScribeSpotCheckList.checklist.md` — the seat that owns the round's full list —
instead of reproducing a competing eight-item list (peer `ScribeSpotCheckList`, 2026-10-26); the
C1 red control names the 40-character r38 judged head per claims erratum E2; and the assimilation
bullet records which three of the seven refusal flips were sampled.

## Evidence — commands run and their output

### 1. Claims, controls, lane state (read-only)

```
$ git -C kasegi-shokunin log --oneline -3
d65d823 round-39: wave1 spec/dispatch
dcd3170 round-39: claims freeze C1/C2 + controls
480b1a5 round-38 verifier spot-check (integrator, hyaku): non-author admit/reject
$ cat .ufo/waves/round-39/c2-controls/before.txt
frontier rows: 21 / registry rows: 55 / S057 rows: 0 / knowledge entries: 50
harness: entries=24 pass=24 exit=0 ; binding records=45 bound=45 unbound=0 ; audit expected=50
$ cat .ufo/waves/round-39/census-before.txt
kasegi  W04  S028 duplicate url docs.hackerone.com/... ; kasegi W04 S029 duplicate url eur-lex... ; exit=0
```

`claims.json` read in full (`:raw`); `wave1-spec.json` items inspected for the C2 seats
(`ExecFrontierCapture`, `ScribeRowS057`, `ScribeRowsRejected`, `ScribeEntryF22`) so the Gate points
at the artefacts those seats actually deliver.

### 2. Capture identity — this seat's independent fetch, not re-read from a receipt

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 \
    https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf
status=200 bytes=235270 ; sha256 cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99 ; 2026-10-26T19:31:14Z
$ python3 corpus/instruments/capture-source.py --id S057 --kind pdf --url <same> --out $S/S057.pdf.txt
S057 status=200 fetched_bytes=235270 snapshot_bytes=17971 sha256=11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f utc=2026-10-26T19:31:20Z
$ wc -l -c $S/S057.pdf.txt   ->  275 17971
$ sha256sum .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt
11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f   (275 lines, 17,971 bytes)
```

The seat's own normalization of the PDF is byte-identical (same digest, same length) to the
landed capture, and identical to the independent `ScoutReopenS057.reopen.txt` line
`norm lines=275 bytes=17971 sha256=11c8d6d6…` (`cmp exit 0` there against the capture).

Landing page (metadata only, not the bound snapshot): `curl` status=200 bytes=54453,
sha256 `4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d`; normalized
`capture-source.py --kind html` → 135 lines, 3,497 bytes, sha256
`c868f04a56c4fcc8dcfedc7354b2c65df5e47c8d55caf0f0502005e030360db2`.

Manifest read at `.ufo/waves/round-39/wave1/ExecFrontierCapture.manifest.json`: `path S057.txt`,
`url` = registry URL, `capture_url` = the PDF, `fetched_utc 2026-10-26T19:30:55Z`,
`snapshot_bytes 17971`, `lines 275`, `sha256 == snapshot_sha256 == 11c8d6d6…`.

### 3. Quote block Q1-Q4 — word count and occurrence, measured on the landed capture

```
$ python3  # re.sub(r'\s+',' ',capture); count each quote
Q1 words=25 occ=1   ("Whether, and when, to issue VEX information is a business decision …")
Q2 words=13 occ=1   ("Ideally, when a new vulnerability is disclosed, an “under_investigation” status should be issued.")
Q3 words=16 occ=1   ("VEX information includes timestamps to indicate when the information was first issued and most recently updated.")
Q4 words=20 occ=1   ("Strictly speaking, consumers should not assume the status of an upstream component applies to a product that uses the component.")
```

Anchors verified by line read of the 275-line capture: Q1 at L12-L14 (`Whether,` closes L12),
Q2 at L132-L133 (heading `Status changes` L131, lifecycle completed L134-L135), Q3 at L136-L137
(reaffirmation clause L137-L138), Q4 at L184-L185 (`Status inheritance`, exception L187-L191).
These are the anchors the manifest records (`12`, `132`, `136`, `184`) and the ones the landed row
`ScribeRowS057.row.md` cites (`L12-14`, `L79-81`, `L132-138`, `L184-191`).

`Q3`'s manifest quote is 26 words as a two-sentence block; the Gate quotes only its first
sentence (16 words) and carries the reaffirmation clause as the L137-L138 note, so every quoted
item stays ≤25 words (`corpus/QUALITY.md` Q3).

### 4. Boundary against S055 — the four sentences are absent from the CSAF capture

```
$ python3  # re.sub over corpus/source-snapshots/round-38/S055.txt (272,441 bytes)
0 Whether, and when, to issue VEX information is a business decision
0 Ideally, when a new vulnerability is disclosed
0 VEX information includes timestamps to indicate when the information was first issued
0 Strictly speaking, consumers should not assume the status of an upstream
```

So the Gate's "why this is not S055's ground" line is measured, not asserted.

### 5. Candidates — flip state re-measured this round

```
$ curl -sS -L ... https://docs.oasis-open.org/csaf/csaf/v2.1/os/             -> 404, 41334 bytes, 2026-10-26T19:32:23Z
$ curl -sS -L ... https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html  -> 200, 1231332 bytes, same minute
  grep -oE 'Committee Specification[^<]*|21 October 2026' -> "Committee Specification Draft 04", "21 October 2026"
$ curl ... minimum-requirements-vulnerability-exploitability-exchange-vex -> 200, 49253 bytes, 2026-10-26T19:31:58Z
  normalized page L80 "April 21, 2023"; L81 "This document specifies the minimum elements to create a Vulnerability
  Exploitability eXchange (VEX) document. These elements are derived from, but may not fully conform to, existing VEX
  documentation and implementations."; linked PDF /sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf
```

CSAF v2.1's `os/` artifact is still absent → the round-38 flip condition remains unmet, and a
v2.1 VEX section would supersede S055's ground, not F22's. The Minimum Requirements document
restates S055's element set (it is the document S057 itself cites as background, footnote 1), so
it lands as rejected row `S056`, not as a new frontier candidate.

### 6. Rejected rows — read from the landed row deliverables, cross-checked against live fetches

`ScribeRowsRejected.S056.row.md` / `.S058.row.md` / `.S059.row.md`, each 11 cells / NF=13,
status `rejected`, reason + `flip:` in the `teaches` cell. Live probes this seat ran:

```
$ curl ... https://github.com/openvex/spec/releases/tag/v0.2.0 -> 200, 209727 bytes, 2026-10-26T19:31:58Z
  body: "This is the release of the OpenVEX Specification v0.2.0." … "released this 22 Aug" (no year rendered)
$ curl ... https://cyclonedx.org/docs/1.7/json/ -> 200, 6419901 bytes, 2026-10-26T19:31:59Z
  normalized L16068-L16073: "resolved" / "resolved_with_pedigree" / "in_triage" / "false_positive" / "not_affected"
  L16076 "The rationale of why the impact analysis state was asserted."; L16080 "code_not_reachable"; L16087 "protected_by_mitigating_control"
```

S058's unestablished release date and S059's second vocabulary (six states, nine justifications)
are consistent with the rows' rejection reasons; the flips in the Gate are the rows' own.

### 7. Assimilation package — byte identity and id collisions

```
$ find /home/vgpnk/Projects/shokuknow/merge/kasegi -type f | wc -l          -> 70
$ find ... -printf '%TY-%Tm-%Td %TH:%TM:%TS\n' | sort -u | head             -> 2026-10-24 23:33:20
$ sha256sum .../SOURCES.append.md
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb        (unchanged from rounds 35-38)
$ grep -rliE 'csaf|vex' .../merge/kasegi --include=*.md | wc -l              -> 0
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' .../SOURCES.append.md          -> 94
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' lane/SOURCES.md (+ S056..S059) -> 59 ids
$ comm -12 reg.ids staged.ids | wc -l                                        -> 29   (S031..S059)
$ sha256sum reg.ids staged.ids
b698a2460f64e9a247954e1f9eec005bf4c59058446ae609806362808173ea2f  reg.ids (59)
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged.ids (94)
```

Staged ids S055-S059 are five different documents (Cybozu vulnerability-handling policy, Cybozu
bounty FAQ, pepabo reporting policy, IPA intake page, CNVD weekly) — number collisions only, so
the Gate states 25 → 29 collisions and forbids renumbering into this round's ids.

Three of the seven refusal flips sampled this round, all still unmet:

```
$ sha256sum corpus/knowledge/program-severity-ladders-and-reward-scales.md   -> 6c05c98f… (67 lines)
$ sha256sum .../merge/kasegi/knowledge/corpus/knowledge/program-severity-ladders-and-reward-scales.md
35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87         (50 lines)  -> no byte-identity
$ grep -c newsType_6 corpus/source-snapshots/round-32/S049.txt               -> 0
$ grep -c sse.com.cn corpus/SOURCES.md                                       -> 0   (S047 unregistered)
```

### 8. Head measurements at the current lane tip (d65d823), for this receipt's own audit trail

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                                  -> 21
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        -> 55
$ ls corpus/knowledge/*.md | wc -l                                            -> 50
```

The post-state readings in the Gate (registry 59, frontier 22, harness 25/25, binding 46/46,
audit expected=51, knowledge 51) belong to the instruments at J and were not measurable at this
head; the Gate cites them as the pins a non-author re-derives.

### 9. Claims erratum 1 — read, and E2 verified independently

```
$ git rev-parse 66703aca
66703acaaff50529a35be49aa8759d04140720ad
$ git cat-file -t 66703acaaff50529a35be49aa8759d04140720ad   -> commit
$ git cat-file -t 66703aca50529a35be49aa8759d04140720ad      -> fatal: Not a valid object name
```

`.ufo/waves/round-39/claims-erratum-1.md` (L1 KasegiR39, append-only) sets E1 registry after-count
59 (the claim's 58 was an arithmetic slip) and E2 the r38 judged head to
`66703acaaff50529a35be49aa8759d04140720ad` (the frozen string was 37 chars). Both are confirmed by
the measurements above; the deliverable already stated 55 → 59 and now names the 40-char hash.

## Findings

1. **Registry count — frozen claim vs row deliverables, resolved by erratum E1.** The frozen C2
   counting command expects `58` while the before-control is 55 and the round appends four rows
   (`S057` mined, `S056`/`S058`/`S059` rejected) → 59; `ScribeRowsRejected.registry-changes.md`
   records the same ("Registry 55 rows pre-append → 59 post-append"). Erratum E1 adopts 59. The
   Gate states 59.
2. **r38 judged-head hash — frozen string was not an object; resolved by erratum E2.** The frozen
   `66703aca50529a35be49aa8759d04140720ad` (37 chars) fails `git cat-file -t`; the 40-char
   `66703acaaff50529a35be49aa8759d04140720ad` resolves to a commit. The Gate's red-control bullet
   uses the 40-char form.
3. **Anchor rendering trap, closed by the landed row.** The `ScribeRowS057` item spec supplied
   `pdftotext -layout` line numbers (`PDF L19-20, L129, L205-213, L287-294`); that rendering is
   400 lines and does not address the committed 275-line capture. The landed row names both
   numberings and says the layout one "does not address this 275-line capture"; this Gate pins
   only capture lines (12, 132, 136, 184) so `source-recheck` can resolve every quote.
4. **Stability artifact is consistent.** `ExecCaptureStability.stability.txt` measures three
   renderings (`-layout` 400 lines `d32b961c…`, collapsed-layout 278 lines `03dd22dc…`,
   instrument path 275 lines `11c8d6d6…`) and binds the instrument path — the same digest this
   seat derived independently. No divergence to report.
5. **No competing spot-check list.** `ScribeSpotCheckList` owns the round's full list
   (`wave1/ScribeSpotCheckList.checklist.md`); the Gate points at it and keeps only the four pins
   its own blocks rest on.

## Known limits

- The Gate's red-control bullet restates the C1 receipt contract (`.ufo/waves/round-39/final-gates/all-gates.txt`,
  `closed=8/8`, `selftest cases=8 failures=0`, base and r38-head reds); this seat did not run
  `r39-closure.sh` (it does not exist at this head) and claims no result for it.
- Quote word counts are whitespace-token counts on the pinned sentences; `Q1` sits exactly at the
  25-word bar.
- The Gate's post-state readings (registry 59, frontier 22, harness/binding/audit/knowledge
  counts) are the instruments' values at J, not measurements taken by this seat.
- No tool installs, no upgrades, no pacman, no environment changes: nothing to record under the
  operator's tooling directive.

## Out of scope / untouched

- No product file, lesson, registry, README, PROVINCE, SKILL, SCORECARD, SHONEN, MANIFEST, claim
  or erratum was edited; the only writes are the deliverable above, this receipt, and scratch
  (now removed).
- Read-only git only (`git log`, `git status`, `git rev-parse`, `git cat-file`); no
  add/commit/checkout/reset/stash, no jj.
- Scratch removed and verified: `rm -rf /fast/scratch/hyaku/kasegi-r39/ScribeLessonGate` →
  `test -e` reports `scratch absent: /fast/scratch/hyaku/kasegi-r39/ScribeLessonGate`.
