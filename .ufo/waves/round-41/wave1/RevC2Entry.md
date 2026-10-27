# RevC2Entry — round 41 wave 1 receipt (C2 pre-review: F24 knowledge entry + row deliverables)

Seat: `RevC2Entry` (reviewer, leaf — no subagent dispatch).
Item: pre-review the C2 knowledge entry and row deliverables (ScribeC2Entry / ExecC2Rows)
against `corpus/QUALITY.md`'s admission bar and the two model entries; flag any bar miss.
Reviewed axes: coverage (C2 admission surface), depth:verifiability (of the reviewed bytes).

## 0. Verdict (summary)

**The knowledge entry, capture and manifest record pass the bar on every first-hand check I ran.**
No Q1–Q10/R12 miss found in `ScribeC2Entry.entry.md` (53 lines), `ExecC2Capture.S063.txt`
(842 lines) or `ExecC2Capture.manifest-record.json`. All findings below are either
** splice-time conditions** (the entry is placeholder-marked by design; the landed bytes must
satisfy them) or **integration conditions** on artifacts the L1 still lands. The three
`ExecC2Rows` row deliverables were **not present in `wave1/` at review close** (polled
08:27→08:51 UTC; seat alive — scratch dir present); §6 records the exemplar-derived
acceptance checks for them so the L1 can apply them at integration.

## 1. What I reviewed, and the bar I applied

- `corpus/QUALITY.md` (base 5b29ea14) — entry criteria Q1–Q10, record criteria R12 (recheck
  `--source` coverage), R6/R32 (append-only, declared-block bytes).
- Model entries (per the item spec): `corpus/knowledge/cyclonedx-analysis-subtree.md` (322 lines,
  F23/S060, sha256 5a549e31…) and `corpus/knowledge/cisa-when-to-issue-vex.md` (144 lines, F22/S057,
  sha256 5010a107…) — trio order, `ground:` line, one-command `cd <lane> && source-recheck.py
  --manifest … --source S0xx   # …` recheck family, per-quote anchors, rejected
  over-generalizations, honest limit.
- Round-40 admission exemplars for the row deliverables: `corpus/README.md` L505–543 (r39/r40
  admission appendix blocks), `PROVINCE.md` L72–78 (F17/F18/F20 amendment lines),
  `corpus/SOURCES.md` S057 (L62) / S060 (L63) rows (11-column schema).
- Instruments the landed bytes must satisfy: `source-recheck.py` (B1/B2, digest compare against
  the manifest record's `sha256`), `frontier-recheck-count.py` (rules A/C/E), `capture-binding-check.py`
  (rules A/B/C), `recheck-audit.py` (parse/cwd/paths/cdroot/instrument/own limbs + expected list),
  `scripts/sources-census.sh` validate (E01–E12, W01–W04).

## 2. First-hand verification of the entry (ScribeC2Entry.entry.md)

File under review: `.ufo/waves/round-41/wave1/ScribeC2Entry.entry.md` — 53 lines, 10,983 bytes,
sha256 `5571a1c7a0c3d85b67d19196637d725da4516ba58aa6fdca38e2445e97a84ad3` (re-hashed at review
time 08:34Z; matches the scribe's receipt digest). The file was updated once mid-review
(08:29:04Z, mtime −0300); I re-ran every check on the current bytes after that.

### 2.1 Quote discipline (Q3, Q9) — all clean

Measured directly against the capture bytes (`ExecC2Capture.S063.txt`, sha256
`925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa`):

- **33 distinct `"…"` spans** (the 21 anchored + 12 inline): **0 missing, 0 non-unique,
  0 over 25 words** (max = 25, the §3.1 scope sentence). Every span is verbatim under
  whitespace collapse and occurs exactly once, so Q9's anchor requirement is met
  trivially-unique and the anchors add binding on top.
- **21 `<<<CAPTURE:Lnnn>>>` markers**, strictly ascending capture lines; I independently
  re-derived anchors with a token-level normalizer and reproduce the scribe's §5 pin table
  exactly: L104, 115, 189, 227, 235, 249, 250, 254, 266, 270, 273, 281, 330, 333, 335, 349,
  357, 528, 536, 538, 571. My earlier first-pass line numbers (off-by-one) were a broken
  offset map in my own checker, not an entry defect — sed line numbers confirm the scribe's.
- **Section attributions**: all 24 checked quotes sit in the sections the entry names
  (§1.1 ×2, §2.4, §2.5, §2.5.3 ×2, §2.5.4 ×3, §2.5.5 ×3, §2.5.7, §3 ×4, §3.1 ×2, §5.2, §5.3 ×2,
  §5.5). One apparent miss in my first pass ("researchers MUST ignore…" cited §2.4, I read §2
  from a truncated display) was my transcription error — the entry says §2.4 and the capture
  agrees (sentence at L183, heading §2.4 at L178).
- Paraphrases without quote marks are faithful: e.g. Claim 5's "one file MAY also cover the
  products and services that the publishing organization provides (§3.1)" tracks L349–350
  ("MAY also apply to products and services provided by the organization publishing the file")
  word-for-word in substance.
- Numeric/factual claims all verified in the capture: `Expires: 2021-12-31T18:37:07z` example
  (L274/310/324, pre-publication — "already in the past" holds); HTTP-1.0-or-higher + https +
  text/plain;charset=utf-8 access rules (L338–340); Encryption's three examples incl.
  OPENPGPKEY (L261–262) and openpgp4fpr (L264); IANA Well-Known URIs "permanent" registration
  (§6.1, L628–633); Preferred-Languages conditional MUST and no-repeat rule (§2.5.8, L288–298);
  exactly two unconditional presence MUSTs (§2.5.3 L227, §2.5.5 L273) so "exactly two fields
  are REQUIRED" is true.

### 2.2 Provenance and recheck form (Q1, Q7, Q10, R12) — clean

- Trio + `ground: F24` directly under the H1, in the model order. `source: S063 — <url> —
  capture corpus/source-snapshots/round-41/S063.txt` names the round-41 snapshot path the claim
  requires.
- `recheck:` is one command, `bash -n` rc 0 (scribe §4.3; shape identical to the two model
  entries), `cd <lane-root> &&` prefixed, human note after `#` naming what the output prints
  and the fail-closed exits — a pinned-capture comparison, not a fresh network check (Q7-honest).
- R12: `--source S063` equals the entry's only declared id; the named manifest is round-41's.
- `verified-at: 2026-10-27` with fetch evidence (HTTP 200, 45,129 raw bytes, sha256
  `79d19ce7…`). Consistency note, not a defect: the entry records a fetch at 08:18:54Z while
  the capture's manifest record pins 08:19:23Z — two fetches of the same served body (identical
  raw sha256 across three fetches per both receipts); the manifest's `fetched_utc` (R21) is the
  capture commit's instant and is the one a re-verifier compares.

### 2.3 Substance (Q2, Q4, Q5, Q6) — clean

- Q2: single tier-A row (IETF RFC 9116, kind spec), opened this round; no tier-C anywhere.
- Q4: attribution kept — "Everything below is a rule of this file's format, never a claim about
  any named organization's practice"; Informational status stated in body and honest limit.
- Q5: a falsifiable rule with six limbs (a)–(f), each checkable against the capture (I spot-checked
  (a), (b), (d), (e), (f) against the capture bytes — all hold), plus two named rejected
  over-generalizations with §5.5 as the falsifier. The model entries carry a dedicated
  "Rejected over-generalizations" section; this entry folds them into Claim 7 — same content,
  conforming to the item's ≤55-line budget (53 used). Not a miss.
- Q6: documentation-only; no probing/scanning instructions, no credentials, no private URLs.

## 3. Capture + manifest record review (ExecC2Capture)

- `ExecC2Capture.S063.txt`: 842 lines / 39,301 bytes / sha256 `925512e7…`; whole-document
  capture (no slice); BOM retained as line 1 (disclosed in the record's `normalized` field —
  a house-instrument cosmetic, byte-identical to `capture-source.py --kind text` output).
  No form feeds, no page footers; normalization reproducible across three fetches.
- `ExecC2Capture.manifest-record.json`: `path` stem == id (B1); single `files: ["S063.txt"]`
  (rule A1); `url` = `https://www.rfc-editor.org/rfc/rfc9116.txt` byte-equal to the registry
  token the row must carry (rule B5); `fetched_utc` strict-UTC 2026-10-27T08:19:23Z (rule C);
  `sha256` = the snapshot digest source-recheck compares. 3 pins at anchors 330/270/235 — I
  verified all three against my anchor table (occ=1 each). Family convention check: S060's
  record pins 3, S057's pins 4 — 3 is within convention; the scribe's §5 table holds the
  21-pin extension if the L1 wants the entry's own claims pinned (their §7.2).
- Integration conditions (for the L1, not defects of the reviewed bytes): (i) the entry's
  `source:` splice must use the committed snapshot's stats — "842 lines, 39,301 bytes; sha256
  925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa" — not the raw fetch stats;
  (ii) zero `<<<…>>>` markers may survive in the landed entry; (iii) `corpus/instruments/
  knowledge-expected.txt` must gain the entry path or recheck-audit prints `unexpected=`;
  (iv) the manifest record must be embedded in `corpus/source-snapshots/round-41/manifest.json`.

## 4. Gate block review (ScribeC2Gate.gate-block.txt)

The block's three quotes are verbatim and correctly sized (18/20/15 words per my count; the
18-word §3 quote and the 15-word §5.3 quote both unique in the capture). Its "Limit" paragraph
is honest on both points I checked: Informational-not-Standards-Track (capture L24–25) and
RECOMMENDED-not-MUST for the one-year bound (L270). Same splice conditions as the entry apply.

## 5. Claims-shape review (the frozen C2 claim vs the base tree)

Every C2 counting command was dry-run against base 5b29ea14 (R22-style satisfiability):

| frozen command | base result | satisfiable? |
|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` (23→24) | 23 | yes — one `| F24 |` row in the r41 appendix block |
| `grep -cE '^\| S[0-9]{3,}…' corpus/SOURCES.md` (62→63) | 62 | yes — S063 append; new id, no E03 |
| awk mined-count of S063 (0→1) | 0 | yes — status cell exactly `mined` |
| `grep -rlE '^source: S063' corpus/knowledge` (0→1) | 0 | yes — entry line 3 starts `source: S063 —` |
| `ls corpus/knowledge/*.md` (59→60) | 59 | yes |
| `frontier-recheck-count.py` (26→27) | entries=26 pass=26 | yes — needs F24 row + entry recheck bound to S063 via round-41 manifest (rules A/C satisfied by construction) |
| `capture-binding-check.py` (54→55) | records=54 bound=54 | yes — record satisfies A/B/C (§3) |
| `recheck-audit.py --quiet` (59→60) | lines=59 expected=59 | yes — one entry + one expected-list line |
| `sources-census.sh validate` (exit 0) | exit 0 (W04 ×2 only: S028, S029) | yes — row must be NF=13 (no `|` in cells), kind spec, tier A, status mined, opened 2026-10-27 (E08 present-date), recheck `on-release` (E09 symbolic ✓), used-by path existing at census time (E11), one `https://` token (B4). URL is new to the registry → no new W04. |
| measure 44/44 = 1.000 | 43/43 (r40 lesson value) | yes — S063 mined-with-capture+entry+harness increments numerator and denominator |

Kill-rule clauses I checked against the reviewed bytes: capture failing source-recheck (fails
closed — manifest absent until landed, §4.3 of the scribe's receipt measured exit 2);
manifest unbound (record satisfies binding rules once the row lands); junk twin (the row is
mined WITH capture+entry+harness pass — the O4 class is the mined row lacking these; the
package as reviewed supplies all three). "Any tracked deletion in corpus paths" — all reviewed
appends are appends.

## 6. Row deliverables (ExecC2Rows) — NOT present at review close; acceptance checks

Polled `.ufo/waves/round-41/wave1/` at 08:27, 08:36, 08:39–08:44, 08:46–08:51 UTC: no
`ExecC2Rows.registry-row.txt` / `readme-row.txt` / `province-amendment.txt`. The seat is alive
(scratch dir present under `/fast/scratch/hyaku/kasegi-r41/ExecC2Rows` at 08:51). Per the item's
fallback I reviewed the claims.json shape (§5) and prepared the byte-level acceptance checks the
L1 should apply to the three files at integration, modeled on the round-40 F23 admission
(README L505–543, PROVINCE L72–78, S060 row):

1. **Registry row** — 13 pipe-fields (E01); cells contain no `|`; col 2 source text carries
   exactly one `https://` token byte-equal to `https://www.rfc-editor.org/rfc/rfc9116.txt`
   (capture-binding B4/B5 — the manifest `url` was fixed to this at 08:19Z); kind `spec`,
   tier `A`, status `mined`, opened `2026-10-27`, recheck `on-release`, used-by
   `corpus/knowledge/rfc-9116-security-txt.md`; teaches = one grounded benefit naming the F10
   complementarity; id unique (E03).
2. **README block** — `## Round-41 admission` appendix (same shape as the round-40 block); one
   coverage-map `| Area | Entry | Source basis |` row and one frontier row `| F24 | … | admitted |
   knowledge/rfc-9116-security-txt.md | S063 | <one decision-rule sentence quoting ≤25 located
   capture words> |`; amendment paragraph ending "frontier stands at **24/24 admitted** … F24 at
   round 41"; the `| F24 |` row must match the claim's counting regex `^\| F[0-9]+ \|` with the
   status cell exactly `admitted`.
3. **PROVINCE amendment** — single end-of-file line, prefix-identical to the F17/F18 form:
   `[r41 Frontier amendment, appended 2026-10-27, end-of-file append per R6] F24 — … — admitted
   round 41; entry corpus/knowledge/rfc-9116-security-txt.md (source S063)`. No receipt
   scaffolding may land (R32); declared-block bytes equal a pre-landed declaration if the L1
   records one.

## 7. Findings register

**Bar misses in reviewed bytes: none.** Items the L1 must satisfy at splice/integration
(collectively the "review conditions", each individually fatal to C2 if ignored):

- F-1 (splice): the entry's `source:` line must land with the snapshot stats (842 lines /
  39,301 bytes / sha256 `925512e7…`), and all 21+3 `<<<CAPTURE…>>>` markers must be resolved —
  any survivor is a Q1/Q3 fail and the kill rule's "lacking the provenance trio" clause.
- F-2 (integration): `knowledge-expected.txt` must gain the entry path (else recheck-audit
  `unexpected=` → expected≠60).
- F-3 (integration): the S063 registry row must carry exactly one https token byte-equal to
  the manifest `url`; NF=13; used-by path must exist when census runs (E11).
- F-4 (integration): the manifest record lands embedded in round-41 manifest.json with
  `fetched_utc` strict UTC (already satisfied in the delivered record).
- F-5 (pending review): ExecC2Rows' three files were not reviewable at close; §6's checks
  must be applied at integration. This is the item's only residual gap.
- F-6 (observation, non-blocking): the manifest pins 3 of the entry's 21 anchored quotes
  (family convention: S060=3, S057=4). The scribe's §5 table supports widening if the L1
  prefers the entry's own claims pinned rather than three of them; not required for any
  counting command.

## 8. Method and hygiene

- Read-only review: no lane/fleet/source-tree writes; only this receipt in `wave1/` and scratch
  under `/fast/scratch/hyaku/kasegi-r41/RevC2Entry/` (recreated after a sibling seat's
  over-broad `rm -rf` of the round-41 scratch parent at ~08:46Z removed it; nothing lost —
  deliverables live in the wave dir; ack sent to ExecI8Forge).
- No tool installs/upgrades (none needed; nothing to record). No mutating git/jj. No `pacman`.
- Base measurements in §5 were produced by running the three lane instruments and census
  against the frozen base tree myself (frontier-recheck-count, capture-binding-check,
  recheck-audit, grep/awk counts, sources-census.sh validate), and the quote/anchor checks by
  two independent Python passes (substring-level span check; token-level anchor re-derivation)
  over the capture bytes.
- Scratch dir removed before yield.
