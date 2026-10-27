# ScribeC2Gate — round-41 wave-1 receipt

Seat: `ScribeC2Gate` (leaf, no subagent dispatch). Claim: C2 `coverage` (8, held) — the F24 / S063
admission evidence record. Round-41 lesson `## Gate` block for S063, in the shape of the round-40
S060 block (`corpus/lessons/round-40.md` L104-L125).

## Deliverable

`.ufo/waves/round-41/wave1/ScribeC2Gate.gate-block.txt`

- bytes 2585, lines 30, max line width 101, sha256
  `9b42ce0b920213733da01f55f4c09df78728bc0918a38e3dd089f9c511d83fa3`
- starts at `### Admitted — F24 / S063 (RFC 9116 security.txt)`; contains **no** `## Gate` heading
  (`grep -c '^## '` on the file = 0, `grep -c '^### '` = 1) — the one-Gate rule (round-40 D4) is not
  re-broken; `ScribeLesson` splices it verbatim under its single heading (coordinated by IRC).
- six bullets, mapped on the S060 block: `Row` / `Source / capture` / `Quotes` / `Entry` /
  `Frontier admission` / `Limit`. `recheck on-release` sits in the Row bullet (the cadence the
  `ExecC2Rows` spec fixes for S063); the Entry bullet says only `executable `recheck:`` — as the S060
  block does — so the entry's command text is not asserted here.
- placeholders: 6 × `<<<CAPTURE>>>` (fetch instant, HTTP status, raw bytes, capture line count,
  capture bytes, sha256) + 3 × `<<<CAPTURE:Lnnn>>>` (one per located quote). Everything else is
  final bytes.

## What the block asserts, and what it deliberately does not

Asserts only values the frozen claims fix: S063 kind spec / tier A / mined / opened 2026-10-27 /
recheck on-release / used-by `corpus/knowledge/rfc-9116-security-txt.md`; frontier 23 -> 24 with
F24/24 admitted; the entry's provenance-trio fields (source/verified-at/ground/recheck) and its
section anchors. It asserts **no** harness, binding, audit or census numbers — those belong to the
L1's gate receipt and would drift if duplicated in a lesson.

## Located quotes — verification

Quotes were taken from my own fetch of the same URL the capture seat fetches, then verified against
a BOM-stripped, CRLF→LF normalization of that byte stream: present exactly once after whitespace
normalization, word counts within the ≤25-word bar.

| # | section | words | occurrences in text | placeholder |
|---|---|---|---|---|
| 1 | §3 (Location) | 18 | 1 | `<<<CAPTURE:Lnnn>>>` |
| 2 | §2.5.5 (Expires) | 20 | 1 | `<<<CAPTURE:Lnnn>>>` |
| 3 | §5.3 (Incorrect or Stale Information) | 15 | 1 | `<<<CAPTURE:Lnnn>>>` |

Command and output (scratch, `/fast/scratch/hyaku/kasegi-r41/ScribeC2Gate`):

```
$ python3 - <<'PY'   # extract backticked spans from the deliverable, compare to the RFC text
...
bytes 2585 sha256 9b42ce0b920213733da01f55f4c09df78728bc0918a38e3dd089f9c511d83fa3 lines 30 maxwidth 101
backticked quoted spans 3
  1 words 18 occ 1
  2 words 20 occ 1
  3 words 15 occ 1
CAPTURE scalars 6 line placeholders 3
h2 headings 0 h3 1
bullets 6
```

Line-span cross-check in my normalization (`1122` lines, digits are **not** in the deliverable —
the placeholders stay):

```
§3 words 18 lines 444 - 446
§2.5.5 words 20 lines 347 - 349
§5.3 words 15 lines 726 - 728
```

If `ExecC2Capture` also declares these three as manifest `quotes`, no `anchor` field is required:
`source-recheck.py::anchor_verdict` demands an anchor only for quotes that occur more than once, and
all three are `occurrences=1`. The manifest record remains the place that pins line numbers.

**A quote I refused.** The primary placement sentence (`For web-based services, organizations MUST
place the "security.txt" file under the "/.well-known/" path, …`) is 27 words and its example URL is
split across lines as `https://example.com/.well-` / `known/security.txt`; whitespace-normalized it
reads `well- known/`, so any strict matcher rejects it. The quoted §3 sentence is the tie-break rule
from the same section, unbroken, and carries the discovery requirement a scanner implements.

## Fetch ledger (my own evidence; the capture seat's numbers are authoritative for the placeholders)

Command (twice, scratch cwd, `TMPDIR` set to scratch):

```
curl -sS -L --max-time 90 -A 'kasegi-shokunin/1.0' \
  -w 'HTTP=%{http_code} BYTES=%{size_download}\n' -o rfc9116.txt \
  https://www.rfc-editor.org/rfc/rfc9116.txt
```

| fetch | UTC | HTTP | bytes | sha256 | notes |
|---|---|---|---|---|---|
| 1 | 2026-10-27T08:19:04Z | 200 | 45129 | `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9` | UTF-8 **with BOM**, 0 CR bytes |
| 2 | 2026-10-27T08:21:35Z | 200 | 45129 | `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9` | byte-identical; `content-type: text/plain;charset=utf-8`; `etag: W/"be7f83388b58df04e4d55a1728262778"`; server `date: Tue, 27 Oct 2026 08:21:35 GMT` |

Normalization sensitivity the L1 must reconcile against the manifest record:

- raw bytes: 45129 B, sha256 `79d19ce7…`, `utf-8-sig` BOM present, `\r\n` count 0 (the server already
  serves LF), 1122 newline-terminated lines, last byte `\n`.
- BOM stripped + CRLF→LF: 45126 B, sha256 `4cf00ab716f18e8510939a65250abee90d32605cebfb29dd43bce5380a476dd5`,
  `splitlines()` = 1122.
- Both give 1122 capture lines, so the `<<<CAPTURE:Lnnn>>>` range is 1..1122 either way; the sha256
  and byte cells differ by 3 bytes (the BOM), so splice them from the manifest record, never from the
  raw fetch.

## Findings (for the critic / verifier; none of these is a defect in the deliverable)

1. **The one-year `Expires` window is RECOMMENDED, not REQUIRED.** §2.5.5: "It is RECOMMENDED that
   the value of this field be less than a year into the future to avoid staleness." The capture-seat
   prompt's guess ("the field MUST be no more than a year into the future") is not what the text
   says; the only MUSTs in §2.5.5 are presence and single occurrence. The Limit bullet records this,
   and no claim or entry wording should upgrade it.
2. **RFC 9116 is Informational.** Front matter reads `Category: Informational` and "Status of This
   Memo" says it is not an Internet Standards Track specification. The tier-A basis is §1.2's BCP 14
   discipline ("when, and only when, they appear in all capitals"), not Standards-Track status —
   stated in the Limit bullet so the row's tier is argued, not assumed.
3. **Lower-case modal verbs in §5 are non-normative.** §5.3's "Organizations must use the "Expires"
   field" and its "should" sentences are lower-case, so under §1.2 they do not bind; the normative
   form of the same rule lives in §2.5.5. An entry that cites §5.3 as a requirement would overstate.
4. **`Contact` is the one required field that may repeat** (only `Expires` carries "MUST NOT appear
   more than once"); the Entry bullet reads "Contact and Expires are the only fields that must always
   be present, and Expires must not appear more than once", which matches the text.
5. **Base-state prefix counts hold** (read-only, lane HEAD `b3b08b2`): `grep -cE '^\| F[0-9]+ \|'
   corpus/README.md` = 23; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` =
   62; `grep -c '^## Round-41 admission' corpus/README.md` = 0; `grep -c 'r41 Frontier amendment'
   PROVINCE.md` = 0 — consistent with `c2-controls/before.txt`, so the 23 -> 24 and S063 claims are
   still ahead of the tree.

## Gates / environment

- `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` — green at start (`/tmp` 3%,
  `/var/tmp` 35%, `/fast/scratch/hyaku` 24%); every write stayed under the scratch dir or the two
  wave-1 paths.
- Tooling: nothing installed, nothing upgraded; no `pacman` run. No network access beyond the two
  rfc-editor fetches above.
- No git/jj mutation anywhere; reads only (`git log --oneline -1` → `b3b08b2 round-41: wave-1 build
  spec (60 seats) + dispatch`).

## Touched surfaces

Writes, exactly two:

- `.ufo/waves/round-41/wave1/ScribeC2Gate.gate-block.txt` (deliverable, sha256 above)
- `.ufo/waves/round-41/wave1/ScribeC2Gate.md` (this receipt)

Scratch `/fast/scratch/hyaku/kasegi-r41/ScribeC2Gate/` was used for the fetch, the normalization and
the validation scripts, and is removed before yield (`rm -rf`, verified absent). No lane file, no
fleet-root file, no sibling lane, no source tree, no `.ufo/state/`, no `corpus/` file was modified.

## Out of scope (left to the owning seats)

- The S063 registry row, README coverage-map row and PROVINCE amendment bytes (`ExecC2Rows`), the
  knowledge entry bytes (`ScribeC2Entry`), the capture and manifest record (`ExecC2Capture`), the
  harness/binding/audit/census counters and the C2 kill-rule controls (`ExecControls`, `ExecC2Instruments`,
  wave-2 attack seats).
- The round-41 `## Gate` heading and any section preamble; the round-41 `### Rejected` subsection.
