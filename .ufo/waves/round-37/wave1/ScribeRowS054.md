# ScribeRowS054 — S054 registry row draft + column audit (round 37, C2 coverage)

Seat: `ScribeRowS054` (scribe), leaf. Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane head at drafting: `b362068195d5489aa94b31e6ec8f880c367e0ba0` (round-37 claims-erratum-1).
Frozen claims `.ufo/waves/round-37/claims.json` @ `224df74db2a46d627ae1475a72ca48796bbd177c`; correction read
and applied: `.ufo/waves/round-37/claims-erratum-1.md` (committed at `b362068`).

## 1. Delivered row (verbatim, single line; apply after the `| S053 |` row)

```
| S054 | SSVC: Stakeholder-Specific Vulnerability Categorization — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ | docs | A | CERT/CC's own SSVC documentation: decision-point-based prioritization for vulnerability management | the overview definition sentence at line 247 of capture corpus/source-snapshots/round-37/S054.txt (SSVC rates vulnerabilities on risk to the concerned stakeholder), the categorization opener at line 259, and the outcome/decision-point sections at lines 261-265 and 277-281 | SSVC is a modular decision-point system for prioritizing vulnerability-management actions for a stakeholder — distinct from CVSS severity, KEV catalog status and EPSS likelihood; read each stakeholder model's chosen decision points and outcomes | mined | 2026-10-26 | 90d | corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md |
```

Row bytes 866 including the trailing newline (865 without); sha256 of the row file with trailing newline
`83020b30ca32fd49c2a1cd85864792d01004a594b59ad2f13fb83e1e6f734f03`.
Insertion point measured read-only at `corpus/SOURCES.md:59` (the `| S053 |` row); the row becomes line 60, the
blank line and `## Paths` shift down by one, and no other line changes.

Revision note: the first draft of this row cited only line 259. It was revised to lead with line 247 after the
entry seat's staged manifest was found to pin its Q1 at 247 (same capture bytes, different quoted span); both
lines are definitional and both verify — see §3/§4. The earlier draft (row sha256 `ea4f1676…3111`) is superseded.

## 2. Column-by-column audit

`awk -F'|' '/^\| S054 \|/{print "NF="NF" cells="NF-2}'` on the row → `NF=13 cells=11`.

| # | field | cell as delivered | check |
|---|---|---|---|
| 1 | id | `S054` | `| S05x |` row shape; registry max id today is `S053`, so S054 is the next id; `git log --all -S'\| S054 \|' -- corpus/SOURCES.md` is empty, so the id was never minted as a row |
| 2 | source | `SSVC: Stakeholder-Specific Vulnerability Categorization — https://certcc.github.io/SSVC/tutorials/ssvc_overview/` | exactly **1** `https://` token (rule B4); token byte-identical to the round-37 manifest record `url` (rule B5; §3 A1) |
| 3 | kind | `docs` | registry vocabulary: docs 41 / spec 8 / dataset 2 / paper 1 / community 1 across the 53 existing rows |
| 4 | tier | `A` | registry vocabulary: A 51 / B 1 / C 2 |
| 5 | scope | `CERT/CC's own SSVC documentation: decision-point-based prioritization for vulnerability management` | no `|`; names the owner and the mechanism; claims nothing outside the docs site |
| 6 | anchor | `the overview definition sentence at line 247 of capture corpus/source-snapshots/round-37/S054.txt (SSVC rates vulnerabilities on risk to the concerned stakeholder), the categorization opener at line 259, and the outcome/decision-point sections at lines 261-265 and 277-281` | no `|`; each cited line verified in the capture bytes pinned by the manifest sha256; both quoted sentences occur exactly **1×** (§4) |
| 7 | teaches | `SSVC is a modular decision-point system for prioritizing vulnerability-management actions for a stakeholder — distinct from CVSS severity, KEV catalog status and EPSS likelihood; read each stakeholder model's chosen decision points and outcomes` | no `|`; states the three-way distinction the C2 predicate claims (CVSS severity / KEV status / EPSS likelihood) plus one falsifiable reading rule |
| 8 | status | `mined` | enum present; every one of the 41 mined rows carries a knowledge path, and this row does too |
| 9 | opened | `2026-10-26` | strict ISO date; matches round date and the frozen claim |
| 10 | recheck | `90d` | enum present (90d 15 / 180d 16 / on-release 17 / 730d 4) |
| 11 | used-by | `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` | no `|`; byte-for-byte the entry path the C2 claim names |

Pipe audit: `pipes=12` (2 edge delimiters + 11 cell separators), `escaped=\|` count `0`, so `NF=13` under
`awk -F'|'`. No cell contains a literal or escaped pipe.

## 3. Instrument evidence (scratch fixture; no lane write)

Fixture `/fast/scratch/hyaku/kasegi-r37/ScribeRowS054/root`: copy of lane `corpus/SOURCES.md` with the row
inserted after `| S053 |`, plus `corpus/source-snapshots/round-37/{S054.txt,manifest.json}` copied from the
**entry seat's surviving staged pair** (`/fast/scratch/hyaku/kasegi-r37/ScribeEntryF20/`: capture sha256
`ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`, 32,623 B, 518 lines; manifest sha256
`39bfd72b5059dd10ec0a138cd4b404cb39438bf112c167edb7ef1594fb3418e1`, 1,393 B), plus the used-by target stub.
Instruments were invoked from the lane checkout with `--root`/`--manifest` pointing into the fixture.

| id | command | result |
|---|---|---|
| A1 | `python3 corpus/instruments/capture-binding-check.py --root <fixture>` **with** the row | `MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0` / `AUDIT … multi_row_url=0 orphans=0` / `records=1 bound=1 unbound=0`, `A1_exit=0` |
| A1c | same command, row deleted (control) | `FAIL rule=no-row record=S054 dir=round-37` / `records=1 bound=0 unbound=1`, `control_exit=1`; restoring the row returns `bound=1 unbound=0`, `restored_exit=0` — the row is the instrument-visible hinge and the delivered cell form is the one that binds |
| A2 | `python3 corpus/instruments/source-recheck.py --manifest <fixture>/corpus/source-snapshots/round-37/manifest.json --source S054` | `S054:sha256 OK`; `Q1 OK occurrences=1 anchor=247-ok`; `Q2 OK occurrences=1 anchor=259-ok`; `Q3 OK occurrences=1 anchor=277-ok`; `Q4 OK occurrences=1 anchor=367-ok`; `A2_exit=0` |
| A3 | shape audit on the row | `NF=13 cells=11 pipes=12 escaped=0` |
| A4 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' <fixture>/corpus/SOURCES.md` | `54` (53 + this row) — the C2 counting command's expected value |
| A5 | used-by target present in fixture | `present` (fixture stub only; real entry is §6 dependency) |

A2 independently confirms both line numbers the anchor cell cites: `anchor=247-ok` (Q1) and `anchor=259-ok`
(Q2), plus the decision-point sections' opener `anchor=277-ok` (Q3). Those are the manifest's verdicts, not my
reading alone.

Manifest-generation note: an earlier run of the same two instruments used the capture seat's manifest
(`/fast/scratch/hyaku/kasegi-r37/ExecC2Capture/manifest.json`, 3,989 B, four quotes anchored 259/277/473/68);
that file was removed by its owner and I had not hashed it, so those readings are transcript-only and are not
offered as reproducible evidence. Its capture bytes were the same `ff3f3b2c…`. Both staged manifests agree on
`url`, `sha256`, `lines`, `snapshot_bytes` and on anchors 259/277; they disagree on the remaining quoted spans
(capture-seat set 473/68 vs entry-seat set 247/367). Only the committed manifest is authoritative; my anchor
cell is safe under either because it cites lines that exist in the shared capture bytes.

## 4. Anchor grounding (read against the pinned capture bytes)

Capture: 518 lines, 32,623 bytes, sha256 `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`
— identical to the round-37 manifest record (`snapshot_bytes=32623`, `lines=518`), whose `url` is
`https://certcc.github.io/SSVC/tutorials/ssvc_overview/`.

- L247 (definition sentence, occurs **1×**): `Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability (how likely it is that there will be an exploit), SSVC rates vulnerabilities on risk to the concerned stakeholder. It is not an attempted one-size-fits-all solution. SSVC follows a stakeholder-defined decision model to make these determinations of risk.`
- L259 (categorization opener, occurs **1×**): `SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders. These categories reflect the timeliness of action to be taken. …`
- L261–L265 (outcome categories): `Defer: do not act at present.` / `Scheduled: …` / `Out-of-cycle: …` / `Immediate: …`
- L277 (decision-point/outcome rule): `All decision points and decision outcomes (priority categories) must be explainable to the non-expert. …`
- L280–L281 (first decision point): `Exploitation` / `Exploitation refers to how much evidence currently exists that the vulnerability is being exploited. …`
- L366–L367 (`Exposure refers to how difficult it would be for an attacker to access a system from the open Internet. …`) also checked; not cited, to keep the cell tight.

Re-derivation if the committed capture differs from these bytes:
`grep -n 'SSVC rates vulnerabilities on risk to the concerned stakeholder' corpus/source-snapshots/round-37/S054.txt`
→ one hit (expect 247); same for the L259 sentence (expect 259); update `261-265`/`277-281` if the section
shifted. A byte change also changes `snapshot_bytes`/`lines`/`sha256` in the manifest, which is the tell.

## 5. Conflict reported verbatim (not resolved by me)

Frozen claim C2 and my seat spec both print the capture URL as

```
url https://certcc.github.io/SSVC/, fetched_utc strict UTC
```

`claims-erratum-1.md` (committed `b362068`, filed 2026-10-26T14:04Z before any seat scored) replaces it:

```
It changes the **C2 S054 capture URL literal** from
    https://certcc.github.io/SSVC/            (the docs home page)
to
    https://certcc.github.io/SSVC/tutorials/ssvc_overview/   (the "What is SSVC?" overview tutorial page)
```

and states `The S054 row's source cell, the manifest record's url, and the capture file S054.txt all use the
corrected URL.` I delivered the corrected URL: the appended erratum is the authoritative correction, and rule B5
would otherwise fail (`FAIL rule=url-mismatch record=S054`) against the manifest the capture/entry seats built.
Residual conflict for the canonical judge: the frozen C2 predicate text still carries the home-page literal,
and no file in the round edits it.

Second literal difference: my seat spec's anchor reads `the overview definition sentence (line N in the
round-37 capture S054.txt)`; `N` is filled with `247` (entry-seat Q1) with `259` cited alongside, per §4.

## 6. Dependencies and known limits

- **Capture not committed at drafting.** `corpus/source-snapshots/round-37/` does not exist in the lane at head
  `b362068`, and the capture seat's own scratch copy is gone. The audited bytes survive in peer scratch:
  `/fast/scratch/hyaku/kasegi-r37/ScribeEntryF20/S054.txt` (+ `S054-overview.txt`),
  `/fast/scratch/hyaku/kasegi-r37/RevEntryF20/S054-overview.txt` — all sha256 `ff3f3b2c…`. If the entry/capture
  seat re-fetches before committing, re-run §4's greps; if the bytes change, the manifest's sha256 changes too.
- **used-by target absent at drafting.** `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`
  does not exist in the lane (`corpus/knowledge/*.md` = 48). The cell names the contract path, so no row edit is
  needed when the entry lands, but `mined` is only honest once that entry exists.
- **Id reuse is label-only.** `corpus/lessons/round-35.md:120` uses the token `S054` as a *quarantine label* for a
  different payload (513,648 B PDF, `payload-absent`); no registry row ever carried the id (§2 row 1). There is no
  registry collision.
- Scope of this audit: row shape, enums, pipe count, single-URL binding, and anchor-line existence. I did not
  evaluate entry quality (Q1–Q6), the F20 README admission, the harness, census, or recheck-audit expected=49 —
  those belong to the entry/capture/verifier seats. I did not edit the frozen claims or the erratum.

## 7. Touched surfaces

- Writes: `/fast/scratch/hyaku/kasegi-r37/ScribeRowS054/` (fixture root, `row.txt`, `SOURCES-with-row.md`,
  `audit.log`) and this receipt only. Scratch removed after filing.
- Reads only: lane repo (`corpus/SOURCES.md`, `corpus/instruments/{capture-binding-check,source-recheck}.py`,
  `corpus/instruments/README.md`, `corpus/lessons/round-35.md`, `.ufo/waves/round-37/*`), peer scratch dirs, and
  read-only git (`rev-parse`, `log -S`, `status`).
- No mutating git/jj command, no repo/sibling-lane/source-tree write, no tool install or upgrade, no swarm, no
  `agent://all` message.

## 8. Findings for the L1

1. Apply the row verbatim after `| S053 |`; the 11 cells are audited. Open ends: capture commit (§6.1) and entry
   file (§6.2).
2. The row is the hinge for C2's binding evidence: without it the round-37 manifest fails
   `FAIL rule=no-row record=S054` and `bound=0` (A1c), so capture-binding-check's `bound=1` depends on this exact
   URL text.
3. Two staged manifests for the same capture bytes pin different quoted spans (473/68 vs 247/367). Only one can be
   committed; the entry seat's (`39bfd72b…`) is the one my A2 run verified against, and the row cites 247/259/277,
   which both variants already anchor.
4. Erratum-vs-claim URL conflict (§5) needs the canonical judge's ruling; I followed the erratum, which is also
   what the manifest bytes require.

Report: `.ufo/waves/round-37/wave1/ScribeRowS054.md`
