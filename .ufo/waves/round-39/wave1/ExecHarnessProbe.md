# ExecHarnessProbe — frontier-recheck-count.py semantics on a scratch mirror (round 39)

Seat: ExecHarnessProbe (leaf executor). Axes touched: depth:verifiability (C1 evidence shape), coverage (C2 F22 admission).
Item: probe `corpus/instruments/frontier-recheck-count.py` on a `git archive` mirror of the lane plus F22 artifacts,
so the F22 admission lands clean when the L1 re-runs on the integrated tree. Deliverable:
`.ufo/waves/round-39/wave1/ExecHarnessProbe.harness.txt`.

## Deliverable

| path | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-39/wave1/ExecHarnessProbe.harness.txt` | 887 | 74,637 | `ecd856f8e548ebe0a9cf3bb9ad49576f2f3cef6894ac0c0207ff7d6f80487a53` |

Sections A-G were filed first (815 lines, 68,700 bytes, sha256 `5bacb768d2eaec0798e37772e60d9a938f4ab599554cd1e0047857e8ff31d7b2`); section H was
appended after the sibling deliverables landed, and the pre-H bytes still hash to that value.

It is a transcript of the probe: every command line, its verbatim stdout/stderr and its exit code, plus a
section G that maps each cut to the exact `problems=` string the harness printed.

## Mirror and harness provenance

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse 480b1a505a2dfc14a4f718d16d63808247214d0a
480b1a505a2dfc14a4f718d16d63808247214d0a
$ git -C <lane> archive 480b1a5… | tar -x -C /fast/scratch/hyaku/kasegi-r39/ExecHarnessProbe/mirror     # 7 corpus/ entries, 50 knowledge entries, no .git
$ sha256sum mirror/corpus/instruments/frontier-recheck-count.py        # == lane copy
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249
$ python3 mirror/corpus/instruments/frontier-recheck-count.py --selftest --scratch <scratch>
selftest case=bidirectional-holds exit=0 want=0 verdict=pass
selftest case=selection-not-declared exit=1 want=1 verdict=pass
selftest case=header-source-not-rechecked exit=1 want=1 verdict=pass
selftest case=evidence-list-declares-selection exit=0 want=0 verdict=pass
selftest case=evidence-declared-not-rechecked exit=1 want=1 verdict=pass
selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=pass
selftest cases=6 failures=0
```

The harness bytes probed are byte-identical to the lane's, so the semantics below are the landable ones.
Python 3.14.8. Nothing was installed; `pdftotext`/`curl` were already present, so no tooling change to record.

## F22 fixture applied to the mirror (mimics the intended after-state)

Fetch (curl `-sS -L --max-time 90 -A kasegi-shokunin/1.0`, 2026-10-26T19:31:25Z):
`When-to-Issue-a-VEX-508c.pdf` status=200 content-type=application/pdf bytes=235270
sha256 `cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99`; publication page status=200
text/html bytes=54453 sha256 `4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d`. Both match the
round-38 ScoutVexLeads ledger exactly.

Artifacts written into the mirror only (never the lane):
`corpus/source-snapshots/round-39/S057.txt` produced by the lane's own `capture-source.py pdf_to_text()`
(pdftotext `-enc UTF-8` + `collapse()`): 275 lines, 17,971 bytes, sha256
`11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f`; `.../round-39/manifest.json`
(schema_version 1, one S057 record, 6 pinned quotes Q1-Q6 with anchors 13/79/132/137/182/120);
`corpus/knowledge/cisa-when-to-issue-vex.md` (`source: S057 — …`, `verified-at:`, `ground: F22`, one `recheck:`
line, body citing S057.txt line numbers plus S052/S053/S054/S055/S056 in prose); README end-of-file append
(coverage-map row + F22 admitted row); SOURCES S057 row (inert for this harness — it reads only
`corpus/README.md`, the entry, the manifest and the capture).

Baseline run on the mirror (section A of the transcript):

```
PASS     F22  knowledge/cisa-when-to-issue-vex.md                  ids=S057           exit=0
entries=25 pass=25 exit=0
$ … --json <scratch>/v-base.json   →  "status": "PASS", "problems": [], "declared_ids": ["S057"], "recheck_ids": ["S057"]
```

The 24 pre-existing rows stay PASS with it, which is the exact claimed shape.

## Cut limbs — one cut per copy, exact harness strings (transcript §G)

| cut | F22 line | summary | process exit |
|---|---|---|---|
| baseline | `PASS … ids=S057 exit=0` | `entries=25 pass=25 exit=0` | 0 |
| no entry (`missing-entry`) | `FAIL … ids=- exit=- problems=missing-entry` | `entries=25 pass=24 exit=1` | 1 |
| no manifest | `FAIL … ids=S057 exit=- problems=manifest-unreadable` | `entries=25 pass=24 exit=1` | 1 |
| truncated manifest JSON | `FAIL … problems=manifest-unreadable` | `entries=25 pass=24 exit=1` | 1 |
| no capture | `FAIL … ids=S057 exit=2 problems=recheck-exit-2` (exec: `S057:source UNAVAILABLE reason=missing`) | `entries=25 pass=24 exit=1` | 1 |
| recheck swapped to `--source S054` | `FAIL … problems=header-sources-not-rechecked,selection-not-declared-by-entry,manifest-missing-ids` | `entries=25 pass=24 exit=1` | 1 |
| S054 cited in prose, binding S057 | `PASS … ids=S057 exit=0` | `entries=25 pass=25 exit=0` | 0 |
| S057 declared but never cited in prose | `FAIL … problems=selection-not-cited-by-entry` | `entries=25 pass=24 exit=1` | 1 |
| body bullet `- S054, "…": "…"` | `FAIL … problems=header-sources-not-rechecked` | `entries=25 pass=24 exit=1` | 1 |
| recheck comment carrying `--source S054` | `FAIL … problems=selection-not-declared-by-entry,manifest-missing-ids` | `entries=25 pass=24 exit=1` | 1 |
| recheck line is `--selftest` | `FAIL … problems=not-a-recheck-invocation,no-source-selection,no-manifest` | `entries=25 pass=24 exit=1` | 1 |
| status cell `admitted (provisional)` | F22 row not read at all | `entries=24 pass=24 exit=0` | 0 |
| F22 row absent | F22 row not read at all | `entries=24 pass=24 exit=0` | 0 |
| F23 row on the same entry | both rows PASS, `DUPLICATE-ENTRY F22,F23 knowledge/cisa-when-to-issue-vex.md` | `entries=26 pass=26 exit=1` | 1 |
| stale `recheck:` line in a fence above the header | `FAIL … problems=header-sources-not-rechecked,selection-not-declared-by-entry,manifest-missing-ids` | `entries=25 pass=24 exit=1` | 1 |
| real recheck line duplicated in a body fence | `PASS … ids=S057 exit=0` | `entries=25 pass=25 exit=0` | 0 |

`source-recheck.py` exit codes seen directly: 0 (sha256 OK + Q1-Q6 `OK normalized=markup-whitespace
occurrences=1 anchor=N-ok`), 2 (`S057:source UNAVAILABLE reason=missing`), 2 (`manifest UNAVAILABLE
reason=unreadable-or-invalid`). Missing capture and unreadable manifest are both 2; a moved quote would be 1.

## Landing rules for the L1 (derived from the rows above, not from the docstring)

1. **The entry must cite S057 in prose.** `source: S057` and the `recheck:` line are declarations/commands and
   are explicitly excluded from the citation set; without a body mention (e.g. `(S057.txt:79-81)`) the row reds
   `selection-not-cited-by-entry` even though every other limb is correct. My first fixture hit exactly this.
2. **Never start a body list item with an S-id** unless that id is also in the recheck selection: `- S054, …`
   is a declaration (evidence-bullet shape), and it reds `header-sources-not-rechecked`.
3. **No `--source`/`--manifest` tokens in the recheck trailing comment.** The whole line after `recheck:` is
   scanned; a comment mentioning `--source S054` turns into a second selection and reds the row.
4. **The first `recheck:` line in the file wins**, fences do not matter. A fenced sample above the header
   silently replaces the real command; an identical duplicate further down is harmless.
5. **The status cell must be exactly `admitted`.** `admitted (provisional)`, or a missing F22 row, drops F22 from
   the run and still prints `entries=24 pass=24 exit=0` — a green that covers nothing. Any round-39 receipt must
   show `entries=25 pass=25 exit=0` **and** the literal `PASS F22 … ids=S057` line, not the summary alone.
6. **`pass=` is not the verdict; the process exit is.** A duplicate entry prints `entries=26 pass=26 exit=1` with
   `DUPLICATE-ENTRY` underneath.
7. **Manifest shape is harness-checked before the exec runs:** absent, unparseable, non-`schema_version: 1`, or
   missing `sources[].id` all give `manifest-unreadable` with `exit=-` (the recheck never executes). A manifest
   that parses but omits the selected id gives `manifest-missing-ids`.
8. **The `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` prefix moves the exec limb off `--root`.** With the
   landed absolute cd, the harness binds rules A-B against `--root` but runs `bash -c` from `--root` *and then*
   cds into the lane, so mirror state cannot satisfy or red the exec limb: my mirror carrying every F22 artifact
   reds `recheck-exit-2` today (§B) purely because the lane is still pre-landing. Consequence: the entry, the
   manifest and the capture must land in the same commit (entry first → red), and no mirror-only run can certify
   the exec limb — the L1's post-integration run must be against the lane.
9. **Quote anchors that verified against my regenerated capture** (useful cross-check for the entry/capture
   seats): business decision L12-L15 (anchor 13), strict-protocol sentence L79-L81 (79), under_investigation
   lifecycle L131-L135 (132), timestamp reaffirmation L136-L138 (137), inheritance warning/exception L182-L191
   (182), threat/`action_statement` L120-L122 (120), KEV pointer L127-L130. My snapshot's numbers (275 lines,
   17,971 bytes, sha256 `11c8d6d6…`) come from the lane's own `pdf_to_text()` on the PDF the round-38 ledger
   names; if the capture seat's landed bytes differ, the manifest must bind the landed bytes, and only the
   anchor line numbers need re-reading.

## Post-filing cross-check against the sibling deliverables (transcript §H)

After this seat filed, `ScribeEntryF22.entry.md`, `ExecFrontierCapture.S057.txt`/`.manifest.json`,
`ScribeFrontierF22.readme.append.md` and `ScribeRowS057.row.md` were present in the wave dir, so the after-state
was rebuilt from their actual bytes instead of my stand-ins (git archive BASE, deliverables copied in verbatim;
hashes in §H show the mirror copies equal the wave-1 files).

- Entry `5010a107cc7ef34bcd7e8d1a74eb2a2bb2a71c3ea666577506d7c2f93dc25d29` (144 lines); capture
  `11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f` (275 lines, 17,971 bytes);
  manifest schema_version 1, ids `['S057']`, 4 pinned quotes.
- **The landed capture is byte-identical to the one this probe regenerated in §A** (same sha256, same
  275/17,971 counts), so the entry's bound digest is the landed digest — no reconciliation is left open.
- Run on the assembled tree with the entry bytes untouched:
  `FAIL F22 knowledge/cisa-when-to-issue-vex.md ids=S057 exit=2 problems=recheck-exit-2`, `entries=25 pass=24 exit=1`.
  The only problem is the exec limb (the lane still does not carry the artifacts), so every rule the harness
  applies **before** exec — declaration set, prose citation of S057, evidence-bullet declarations, comment scan,
  manifest schema and ids — is clean for the landed entry. It reds exactly as rule 8 predicts (entry without
  capture); the row does not need an entry change, only co-landing.
- With the cd prefix repointed at the same tree (the `diff -u` in §H is the entire delta — one line, the cd path):
  `PASS F22 … ids=S057 exit=0`, `entries=25 pass=25 exit=0`, exit 0, and the exec prints
  `S057:sha256 OK` plus `Q1 anchor=12-ok`, `Q2 anchor=132-ok`, `Q3 anchor=136-ok`, `Q4 anchor=184-ok`
  (the entry's own anchor set; my §A fixture pinned 13/79/132/137/182/120 — both verify, nothing to reconcile).
- No second `recheck:` line exists in the entry, and no body list item starts with a foreign S-id, so rules 2
  and 4 are satisfied by the landed text; only the shape rules I listed above had to be checked, and they pass.

## Constraints observed

- Mirror and all work copies under `/fast/scratch/hyaku/kasegi-r39/ExecHarnessProbe/`; `TMPDIR` bound there;
  scratch removed before this receipt was filed (G6), after the deliverable was copied into the wave dir.
- No mutating git/jj anywhere: the mirror is a `git archive` pipe, and the only further git call was
  `git -C <lane> rev-parse 480b1a5…` (read-only). Lane guard at the end of the transcript:
  `git -C <lane> status --porcelain | grep -v '^?? \.ufo/'` prints `(no tracked or corpus change)`, and
  `corpus/source-snapshots/round-39` still does not exist in the lane.
- Wrote only `.ufo/waves/round-39/wave1/ExecHarnessProbe.harness.txt` and this receipt.

## Risks / blockers

- The A-G fixture entry/manifest are probe stand-ins, not the scribe/capture deliverables; §H now measures the
  real ones and the stand-in capture turned out byte-identical, so the stand-in numbers were not a source of
  drift.
- Residual uncertainty (resolved as far as this seat can reach): the landed entry's four quotes verify against
  the landed capture (§H), and the binding limbs are clean. What remains is an ordering obligation for the L1,
  not a defect: land `corpus/knowledge/cisa-when-to-issue-vex.md`, `corpus/source-snapshots/round-39/S057.txt`
  and `.../manifest.json` in the same tree, then run the harness against the lane — entry-first reads
  `recheck-exit-2`.
- One correction to my own earlier peer note: the `S057.txt:79-81` token I attributed to the README append's
  cell 6 exists only in my §A-G fixture row, not in `ScribeFrontierF22.readme.append.md` (`grep -c 'S057.txt'`
  there is 0). The append block's row still parses under the harness regex as `F22` / `admitted` /
  `knowledge/cisa-when-to-issue-vex.md`, which is the property that matters.
