# ScoutLeads — round-42 wave1 receipt

- Seat: ScoutLeads (leaf scout; no subagents used)
- Assignment: re-open the two standing leads and verdict whether their rejection flips fired (probe pattern per round-41/40 receipts)
- Lane repo: /home/vgpnk/Projects/shokunin/kasegi-shokunin (only lane repo; fleet root and shokuknow untouched)
- Verdicts: **S062 (OASIS CSAF v2.1 os/ flip): STANDS** — **S061 (CISA VEX Status Justifications PDF): STANDS**

## Deliverable

- `.ufo/waves/round-42/wave1/ScoutLeads.txt` — 19 lines, 4453 bytes, sha256 `7f8c22e6e2dbc25d7a40e6d7e18dca0aed997e84870e35cd3362b14174004a22`
- Contents: landable verdict report only (fetch ledger + verdict + next recheck per lead). No validation tables inside the deliverable.

## Lead 1 — S062 OASIS CSAF v2.1 os/ flip monitor → STANDS (flip not fired)

All four probes byte-identical to the round-41 ledger (zero drift; round-41 was itself identical to round-40):

| probe | HTTP | bytes | sha256 | fetch UTC |
|---|---|---|---|---|
| `https://docs.oasis-open.org/csaf/csaf/v2.1/` (listing) | 200 | 1097 | 5e59949c479ca03097be81259cb5bf168a857562991c73be3c826e7822f03775 | 2026-10-28T11:02:46Z |
| `.../v2.1/csaf-v2.1.html` | 200 | 1231332 | fdb4bf015c75f01269c1ba346912fd558e8a168b607279b951b1fe5335f366b0 | 2026-10-28T11:02:47Z |
| `.../v2.1/os/` | 404 | 41334 | e416b40032482d96f55c61e3ce3dd871e980c9ff5b4bfa2f89d1c2863fcfd731 | 2026-10-28T11:02:47Z |
| `.../v2.1/os/csaf-v2.1-os.html` (flip target) | 404 | 41334 | e416b40032482d96f55c61e3ce3dd871e980c9ff5b4bfa2f89d1c2863fcfd731 | 2026-10-28T11:02:47Z |

- Listing entries unchanged: csaf-v2.1.{html,md,pdf} (21-Oct-2026), csd01/ (28-May-2025), csd02/ (25-Feb-2026), csd03/ (11-Sep-2026), csd04/ (21-Oct-2026), schema/ — **no os/ entry** (`grep -c 'href="os/"'` → 0).
- Page front matter unchanged: h1 "Common Security Advisory Framework Version 2.1", h2 "Committee Specification Draft 04", h2 "21 October 2026". The ten "OASIS Standard" string occurrences (`grep -o | wc -l` = 10) are the v2.0 bibliographic reference (dated 18 November 2022) and the generic OASIS Standards Final Deliverable boilerplate — not this document's stage.
- Flip condition requires os/csaf-v2.1-os.html → HTTP 200 with front matter "OASIS Standard"; it still returns 404. The only OASIS Standard remains v2.0 (S055).

## Lead 2 — S061 CISA VEX Status Justifications PDF → STANDS (flip not fired)

- `https://www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf` → HTTP 200, 313386 bytes, content-type application/pdf, sha256 `9a4027c68674a99678bfd18d0897cdb213a2db59b568054b2b86439ff0cf513f`, fetched 2026-10-28T11:02:47Z — **matches the recorded hash** and byte-identical to the round-41/40 fetches.
- pdftotext -layout extraction: sha256 `2b480ac832a62cf96bba44670dcdac8089f995d5cf6149b499cbcf00cf8df4e6` — byte-identical to round-41's extraction (273 lines by wc -l; sha256 is the authoritative check and it matches).
- Reachability confirmed; content stable.
- Five labels still in the fresh PDF (pdftotext L51-L55): Component_not_present, Vulnerable_code_not_present, Vulnerable_code_cannot_be_controlled_by_adversary, Vulnerable_code_not_in_execute_path, Inline_mitigations_already_exist. Section 3.7.3 distinction still present (L204-L214).
- Five labels still carried normatively by S055's round-38 capture `corpus/source-snapshots/round-38/S055.txt` (sha256 `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`, 5146 lines, byte-identical): L1762 "The values MUST be used as follows:" governs the label list L1757-L1761 and per-label definitions L1763-L1769; schema label enums at 3091/3127/3133.
- The round-40 rejection rationale (labels already normative in S055; no lane ground needs the 3.7.3 distinction) still holds → rejection stands.

## Commands run (transcript)

All fetches used `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0` from scratch dir `/fast/scratch/hyaku/kasegi-r42/ScoutLeads` with `TMPDIR` bound there. Disk guard was green before the pass (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit=0, /fast/scratch/hyaku 27% used).

```
=== FETCH 1: CSAF v2.1 directory listing ===   2026-10-28T11:02:46Z
HTTP 200 bytes=1097 url=https://docs.oasis-open.org/csaf/csaf/v2.1/
5e59949c479ca03097be81259cb5bf168a857562991c73be3c826e7822f03775
=== FETCH 2: CSAF v2.1 page (csaf-v2.1.html) ===   2026-10-28T11:02:47Z
HTTP 200 bytes=1231332 url=https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html
fdb4bf015c75f01269c1ba346912fd558e8a168b607279b951b1fe5335f366b0
=== FETCH 3: probe os/ directory ===   2026-10-28T11:02:47Z
HTTP 404 bytes=41334 url=https://docs.oasis-open.org/csaf/csaf/v2.1/os/
e416b40032482d96f55c61e3ce3dd871e980c9ff5b4bfa2f89d1c2863fcfd731
=== FETCH 4: probe os/csaf-v2.1-os.html ===   2026-10-28T11:02:47Z
HTTP 404 bytes=41334 url=https://docs.oasis-open.org/csaf/csaf/v2.1/os/csaf-v2.1-os.html
e416b40032482d96f55c61e3ce3dd871e980c9ff5b4bfa2f89d1c2863fcfd731
=== FETCH 5: CISA VEX Status Justifications PDF ===   2026-10-28T11:02:47Z
HTTP 200 bytes=313386 content_type=application/pdf url=https://www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf
9a4027c68674a99678bfd18d0897cdb213a2db59b568054b2b86439ff0cf513f
pdftotext exit=0  extraction sha256 2b480ac832a62cf96bba44670dcdac8089f995d5cf6149b499cbcf00cf8df4e6
```

S055 capture grep (read-only, lane repo):

```
$ grep -n -i -E "component_not_present|vulnerable_code_not_present|vulnerable_code_not_in_execute_path|vulnerable_code_cannot_be_controlled_by_adversary|inline_mitigations_already_exist" corpus/source-snapshots/round-38/S055.txt
1757:component_not_present
1758:inline_mitigations_already_exist
1759:vulnerable_code_cannot_be_controlled_by_adversary
1760:vulnerable_code_not_in_execute_path
1761:vulnerable_code_not_present
1762:The given values reflect the VEX not affected justifications. See [VEX-Justification] for more details. The values MUST be used as follows:
1763-1769: (per-label definitions)
3091/3127/3133: (schema label enums)
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  S055.txt  (5146 lines, 272441 bytes)
```

## Tooling

- No installs/upgrades needed this seat. Tools used: curl (system), pdftotext (system, poppler), sha256sum/wc/grep (coreutils). Nothing installed; nothing written to any PATH directory.
- Network fetches: 5 total (4 docs.oasis-open.org, 1 cisa.gov), all recorded above with HTTP status, bytes, UTC time per the seat spec.

## Hygiene

- Wrote only: `ScoutLeads.txt` (deliverable) and this receipt in `.ufo/waves/round-42/wave1/`. No lane/fleet/shokuknow source files edited; no mutating git/jj commands run (read-only git/grep only).
- Scratch dir `/fast/scratch/hyaku/kasegi-r42/ScoutLeads` removed before yield (fetch artifacts `csaf-v21-dir.html`, `csaf-v21.html`, `csaf-v21-os-dir.html`, `csaf-v21-os.html`, `VEX_Status_Justification_Jun22.pdf`, `vex.txt` were scratch-only; all hashes preserved in this receipt).
