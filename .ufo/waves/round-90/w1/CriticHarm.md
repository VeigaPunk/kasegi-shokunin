# CriticHarm — round-90 harm guard (attack seat)

Base `6088c3eb0c29040415c69e7b5fb91e110480ab26`; freeze `33f43db99c06e89bb9fb78c538313e9450da649f`;
C1 landing `4a7e676895d3fc74e18c853457c9b465ade2ddf5`; C2 landing `643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2`;
receipts `779062a3676cc6b10bf855f18ff897baf0cc6fd5`. Claims are judged only on their frozen predicates; everything
below is a routed defect/qualifier, never a re-score. I edited nothing outside this wave directory.

Receipts beside this file, all commands re-runnable from the lane root:
`CriticHarm-receipts/CriticHarm-d1-density.txt`, `…-d2-callers.txt`, `…-d2b-c2-instrument.txt`,
`…-d3-c1-contradiction.txt`, `…-d4-sources.txt`.

| # | Item | Verdict |
|---|---|---|
| 1 | depth:density guard (SKILL.md, PROVINCE.md untouched; instrument reading) | **NO HARM** |
| 2 | Caller guard (imports/invocations of `capture-source.py`; moved line citations) | **NO HARM** (Q4: two frozen lesson pointers) |
| 3 | C1 — repointed site citing a range that contradicts its own row | **HARM — F1** (2 sites: 158, 439) |
| 4 | SOURCES S131/S132 well-formedness + census validate | **NO HARM** (Q3: S131 status flip pending integration) |

---

## F1 — HARM (depth:verifiability; routed defect): two C1 repoints now cite a range that refutes their own row

The frozen selection rule admits a site when the round-89 label says WRONG with a supported range, minus sites whose
*label reason* says the row content is stale (`claims.json`; `excluded.tsv`). Two admitted sites carry a SUPERSEDES gloss
that the target entry itself has already corrected, so the new range contradicts the sentence it is cited for:

- `corpus/knowledge/triage-thresholds.md:158` — `SUPERSEDES: \`corpus/knowledge/mission-control.md:61-64\` — that entry
  lists 3 signatures, omitting \`usage_limit_reached\``.
- `corpus/knowledge/triage-thresholds.md:439` (§9.7) — `\`corpus/knowledge/mission-control.md:61-64\` (three signatures)`.

The cited range at the same landing commit (`mission-control.md` is unchanged in the whole round — not a diff path):

```
61  - **`detectLimit()`**: tails `fleets/run/*.log` modified <15 min; strict
62    signatures — FOUR, round-13 correction (`usage limit has been reached`,
63    `usage_limit_reached`, `rate limit exceeded`,
64    `429 Too Many`; fleet-dispatch.mjs:272) ANDed with a model-family regex — …
```

Line 62 says **FOUR, round-13 correction**; line 63 **contains** `usage_limit_reached`. The row says the entry omits
exactly that. The round-89 label itself already named the range as stating four signatures
(`tranche5-labels.tsv`: `…:158 WRONG corpus/knowledge/mission-control.md:61-64 four signatures are L61-64`), so the
information that the range refutes the gloss was in the map's own inputs.

Reproduce (one command per line, from the lane root):

```
git show 4a7e676:corpus/knowledge/triage-thresholds.md | sed -n '158p;439p'
git show 4a7e676:corpus/knowledge/mission-control.md | nl -ba | sed -n '61,64p'
git show 02b6d88f:.ufo/waves/round-89/w1/ReviewC1Labels-receipts/tranche5-labels.tsv | awk -F'\t' '$2 ~ /triage-thresholds.md:(158|439|155)$/'
```

Why it is the same class the rule already excludes: site 155 (excluded, frozen) reads
`the SUPERSEDES premise is stale (entry already carries the openai-codex correction); a repoint would cite a range that
contradicts the row`. Sites 158/439 have exactly that condition — the premise ("3 signatures, omitting
`usage_limit_reached`") is stale because the entry carries the round-13 FOUR correction — but they were admitted because
the frozen key is the label-reason *text*, and their label reasons name the range without the staleness note. The labels
confirm the shape: site 152 was excluded for partial support, 155/438 for a stale premise; 158/439 are the stale-premise
case with no note.

Before the landing the same clause was merely *unsupported* by its citation (base `mission-control.md:41-43` is P20/P21
commit-gate text), so the repoint converts an unsupported sentence into a self-refuting one. The landing is otherwise
mechanically perfect: 34/34 map rows equal the label's supported range, every value is present in the landed line, the
old key is gone, every target is in bounds, P3 prints one path, and the map sha256 `7c420856…` equals the pin
(`CriticHarm-d3-c1-contradiction.txt`).

Why the judge cannot see it: C1 P1 is the pinned meter. M9 asserts *value == labelled range* (`LIMB M9 pass rows=34
unbound=none`, `l1/c1-landing-r90.txt`); no limb reads the row text against the range. The predicate can pass while the
two rows mislead a verifier — the exact harm shape of round 89's F1 (a landing that falsifies the entry citing it).

Impacted axis: depth:verifiability (the axis C1 targets). Both sites are inside the 34-site map, so a later "34/34
repointed" reading would inherit the contradiction.

Smallest safe correction (round 91 — the landing is frozen; no target-entry edit needed):

- `:158` → `MATCHES: \`corpus/knowledge/mission-control.md:61-64\` (entry corrected in round 13; it lists four
  signatures incl. \`usage_limit_reached\`)`.
- `:439` → `(entry lists four; corrected in round 13)`.
- Selection rule for later tranches: treat a SUPERSEDES row whose premise the target entry already corrects as
  content-stale, whatever the label reason says — or add a semantic limb to the meter that greps the parenthetical
  against the range. Do not re-freeze this round.

---

## Qualifiers (not harm)

**Q1 — C2 named limit, measured: a bare partner-pattern token passes the gate.** A clean HTML capture carrying a bare
token (the `ghp_` prefix plus 36 alphanumeric characters), with no keyword or separator, goes through the landed gate: rc 0, file written,
0 `INTAKE-REFUSED` lines; the snapshot contains the value (fixture in scratch only; `CriticHarm-d2b-c2-instrument.txt`).
Keyworded forms (`token: <40 chars>`) hit shape `credential`; bare tokens have no shape. The README paragraph added by
the landing states the general limit ("the gate sees only what the scanner's shapes name"), so this is disclosed — but
S131's own subject is GitHub partner patterns, so the L1 should record the class as a named limit rather than let the
claim's phrase "credential material" read as coverage. Coverage axis; no counterexample to any G-limb.

**Q2 — the allowlist is per path *and* per matched bytes, so a routine re-capture at a new round path is refused.**
Measured with the committed snapshot bytes and the landed allowlist (19 rows): `round-89/S128.txt` at its allowlisted
path → `found=0`; the same bytes at `corpus/source-snapshots/round-91/S128.txt` → `found=1
(cloudfront-signed-url-signature)`; `round-87/S124.txt` behaves the same (`authorization`). Consequence: the 180d
recheck of those pages cannot re-capture into a new round directory without adding a new row with a reason. That is the
S131 design (bypass per path, with a stated reason), but the README should say the binding is path-plus-bytes, not
per-source, so the recheck procedure does not read the refusal as a defect.

**Q3 — S131 status flip is a pending integration step, not a landing defect.** S131 is `queued` with `used-by '—'`,
while the landed instrument's docstring (`capture-source.py:22-24`) and `SCORECARD.md:308` name S131 as the design
source, and the round lesson (`corpus/lessons/round-90.md:18`, "admitted, used by the instrument") cites it. CORPUS.md
defines `mined` as cited by ≥1 path in `used-by` (knowledge entries or lessons). C2 P3 excludes `SOURCES.md` from the
landing, so the flip belongs to integration: `queued → mined`, `used-by corpus/lessons/round-90.md` (protocol form; the
round-89 S128/S130 rows used the instrument path instead). Harmless only if it lands — round 89's F1 recorded the same
pending step.

**Q4 — two frozen lesson pointers moved: `capture-source.py:32 → :51`.** `corpus/lessons/round-25-verifier-spotcheck.md:114`
and `corpus/lessons/round-35-verifier-spotcheck.md:107` both write "instrument UA (`capture-source.py:32`)"; the UA moved
from line 32 to 51 because the landing added the intake-gate docstring and imports. CORPUS.md keeps lessons append-only
("corrections are filed here as new entries"), so leaving them is correct; no knowledge entry or README line carries a
moved `capture-source.py` line citation (the only `capture-secret-scan.py` line citations are the round-89-repaired
cloud entry, and that file's bytes did not move in round 90).

---

## Item 1 — depth:density: NO HARM

- `git diff --stat 6088c3e 643ddb4 -- SKILL.md PROVINCE.md` prints nothing; same through `779062a` (receipts only).
  Neither path appears in the 25-path range or in `779062a`.
- Landed readings (`python3 -B corpus/instruments/density.py <file> --label x`):
  **SKILL.md 1251 lines, 38 blocks, mean dens 273.2, 932 path-citation instances**;
  **PROVINCE.md 237 lines, 7 blocks, mean dens 98.5, 31 path-citation instances**.
- Same instrument on the base blobs (`git show 6088c3e:…`) prints identical block/mean/citation numbers, so the
  round moved neither file nor their readings. Landed sha256 `7d082bfe…` (SKILL), `736299ba…` (PROVINCE).

## Item 2 — callers: NO HARM

- No tracked non-`.ufo` file imports the instrument or `capture()`: `git grep -n capture_source` (outside `.ufo/`) and
  the import-regex grep both return nothing. The only `spec_from_file_location` loads are inside
  `capture-source.py` (loads the scanner) and `capture-secret-scan.py` (loads `claim-package-check.py`), plus unrelated
  instruments.
- No tracked code invokes `capture-source.py`. Every hit is a `figure-audit.py` derive-gate **probe string** (the python
  head is refused before execution; the expected rc 35 is the gate's) or a comment. The derive-gate maps are a per-head
  deny list and a head allow list; the new `--allow` option is neither a write nor an ingress option, and `--url`/`--out`
  remain refused, so the maps need no change.
- The signature change is backward compatible: `capture(source_id, url, out, kind, allow_path=None)`; success returns the
  sha256 hexdigest (truthy → `main` 0), refusal returns `None` → `main` 3. `selftest()` calls it with four positional
  args and passes (rc 0). A clean capture through the landed gate is byte-equal to the base instrument's snapshot; a
  credential capture is refused (rc 3, nothing written, existing file kept) while the base instrument writes it.
  (`CriticHarm-d2b-c2-instrument.txt` A–C.)
- Moved line citations outside `.ufo/`: only the two lesson pointers in Q4 (`:32 → :51`); the in-scope class (knowledge
  entries, README lines) is empty.

## Item 3 — C1 contradiction: HARM (F1 above). No other repointed site contradicts its row.

All 34 rows were read against their landed targets (`claim-gates.md`, `mission-control.md`, `ev-model.md`,
`intake-surface.md`, `claim-package-contract.md`). The remaining 32 are consistent with the row text; adjacent worth
noting but not a contradiction: `:251` "matches file text" vs the cited `claim-gates.md:45-46` "every non-symlink file
≤5 MiB, read as UTF-8 — no text/binary filter" (the regex is applied to every file decoded as text, so the phrase is
ambiguous rather than false). Excluded sites 152/155/249/438 are byte-identical to base, so the exclusion was honoured.

## Item 4 — SOURCES: NO HARM

- S131 and S132 are 11-cell rows (`NF=13` with the edge pipes), status vocabulary legal (`queued` / `rejected`), kind
  `docs`, tier `A`; S132 reads `REJECTED: … flip: …`; both have `used-by '—'`.
- S131's anchor resolves: snapshot lines 570 (definition), 572 (block behavior), 610 (bypass requires a stated reason);
  manifest sha256 `0c98d69a…`; `source-recheck.py --manifest corpus/source-snapshots/round-90/manifest.json` rc 0
  (`S131:sha256 OK`, Q01/Q02 anchors ok). The landing receipt also re-captured S131 through the landed gate to scratch
  with the identical digest, so the committed snapshot is reproducible by the committed instrument.
- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
  → **rc 0** (`kasegi ok …/corpus/SOURCES.md`); the only findings are W04 duplicate-URL rows S028/S029/S072/S076/S080/S085,
  all pre-existing, none S131/S132.
- S131 status flip: Q3.

## Counterexample tested (strongest available)

For C2 I hunted a false negative and a false positive rather than repeating the counter's G-limb fixtures: the false
negative is Q1 (a bare partner-pattern token is written), the false positive is Q2 (a legitimate re-capture of an
allowlisted documentation page at a new round path is refused). Both are consequences of the scanner's shape set and the
per-path allowlist, not of the gate wiring; the gate itself refuses before write, keeps an existing file byte-identical,
prints shape and line without the value, fails closed on a scanner/allowlist load error (`gate-error:<ExcType>` path),
and costs ≤0.83 s on an 8 MB text with no pathological pattern found.

## Tooling / hygiene

No tool installed or upgraded; no pacman transaction attempted (host-wide pause respected). Every lane script ran as
`python3 -B`; all fixtures, servers and the base instrument blob lived under
`/fast/scratch/hyaku/kasegi-r90/CriticHarm/`, deleted before this yield (scratch is gone). No credential value was
written into this wave directory: the receipts carry exit codes, shape names, digests and `INTAKE-REFUSED` summary lines
only; the wave files were re-scanned with `capture-secret-scan.py --files` before finishing.

## Files written

- `.ufo/waves/round-90/w1/CriticHarm.md` (this report)
- `.ufo/waves/round-90/w1/CriticHarm-receipts/CriticHarm-d1-density.txt`
- `.ufo/waves/round-90/w1/CriticHarm-receipts/CriticHarm-d2-callers.txt`
- `.ufo/waves/round-90/w1/CriticHarm-receipts/CriticHarm-d2b-c2-instrument.txt`
- `.ufo/waves/round-90/w1/CriticHarm-receipts/CriticHarm-d3-c1-contradiction.txt`
- `.ufo/waves/round-90/w1/CriticHarm-receipts/CriticHarm-d4-sources.txt`
