# ScoutCapBugcrowd — S044/S045 capture reconnaissance (C2 F13)

Seat: `ScoutCapBugcrowd` (scout, leaf). Round 29 wave 1 (hyaku run 7). Lane: kasegi-shokunin.
Scope: reconnaissance for the S044 (Bugcrowd VRT README) and S045 (Bugcrowd CWE crosswalk)
captures — HTTP metadata, line/occurrence tables, cwe.json structure checks, determinism.

Model note: this seat's answering model is the session default `inception/mercury-3`
(workstation project context). No config route table was consulted: every item below is a
deterministic fetch/instrument run — no model-dependent step exists. Item rule 8 records
the model actually run.

## 1. Fetch metadata (raw upstream bytes, 2026-10-25)

Fetches: `curl -sSL` (twice per URL, byte-identical) and `capture-source.py` instrument UA
(`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`, byte-identical).

| source | URL | HTTP | content-type | size_download | by on disk | raw sha256 | git blob sha1 | etag |
|---|---|---|---|---|---|---|---|---|
| S044 | https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md | 200 | text/plain; charset=utf-8 | 8881 | 8881 | `72576250dfff95344cdda7e2af00b3d4843a5785cef9e2af0ab1e251c69ec022` | `dc666d1f5d824c0653f50a745f52c67760a8a559` | `19b012d702e6cadd0604fd7eb521fe4c3207855509a0de50715584736c7fc0b2` |
| S045 | https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json | 200 | text/plain; charset=utf-8 | 28482 | 28482 | `3de912588d845cd57e49dca40e3273b13290c3775b1d6e69b6787efb342ff364` | `19e0805898753b4180f13bb86fd8ad2200d97163` | `86f977325ceb8eb272fd6a7a77b2f7f2370e9cc616579e6fdfa2adb195864556` |

Both matched the expected byte sizes (~8881 B README, ~28482 B cwe.json). Zero redirects.
`capture-source.py` prints a status 200; own curl observed HTTP/2 200.

## 2. README findings (raw upstream line numbers, and landed S044.txt line numbers)

The landed capture `corpus/source-snapshots/round-29/S044.txt` was produced with
`capture-source.py --kind html` (html_to_text): the two `<p align="center">`/`<img …>` badge
blocks are stripped (raw lines 1–8 region), so landed line numbers differ from raw. Exact
map for the load-bearing lines:

| content | raw line | landed S044.txt line | occurrence (landed, normalized) |
|---|---|---|---|
| P1–P5 ladder labels (block) | 62–66 | 34–38 | 1 (exactly-once) |
| Override sentence (full, 35 words) | 25 | 11 | 1 |
| "suggested baseline" scale sentence (19 words) | 60 | 33 | 1 |
| CWE crosswalk link `- [CWE](mappings/cwe/cwe.json)` | 167 | 127 | 1 |
| `#### Supported Mappings` | 164 | 124 | 1 |
| `### Mapping to Other Systems` | 113 | 79 | 1 |
| `#### Priority` heading | 59 | 32 | 1 |
| IDOR varies P4–P1 sentence | 68 | 39 | 1 |
| `null` priority value sentence | 30 | 14 | 1 |
| baseline priority scale (Background) | 15 | 5 | 1 |

P1–P5 ladder labels verbatim (landed L34–38, exactly-once as a 5-line block):
`- **P1**: Critical` / `- **P2**: High` / `- **P3**: Medium` / `- **P4**: Low` /
`- **P5**: Informational` (15 words normalized).

Baseline sentence verbatim (landed L33, occ=1, 19 words):
> The priority represents Bugcrowd's suggested baseline technical severity of the vulnerability on a P1 (Critical) to P5 (Informational) scale.

Override sentence verbatim (landed L11, occ=1). **Note: the apostrophe in `it’s` is
U+2019 RIGHT SINGLE QUOTATION MARK, not U+0027.** A quote typed with a straight ASCII
apostrophe gets `occurrences=0` and source-recheck reports MISMATCH reason=quote-not-found.

> It is important to remember that while the recommended priority, from P1 to P5 might apply without context, it’s possible that application complexity, bounty brief restrictions or unusual impact could result in a different rating.

≤25-word verbatim candidates from the override sentence (both occ=1, landed L11):
- 21 words: `might apply without context, it’s possible that application complexity, bounty brief restrictions or unusual impact could result in a different rating.`
- 17 words: `it’s possible that application complexity, bounty brief restrictions or unusual impact could result in a different rating.`

CWE crosswalk mention is confirmed at landed L127 (`- [CWE](mappings/cwe/cwe.json)`),
under `#### Supported Mappings` (L124).

## 3. cwe.json structure checks (landed S045.txt, parseable JSON)

| claim | result |
|---|---|
| 36 top-level categories | confirmed — `content` array length 36 (20 of 36 have children; 237 total nodes) |
| `idor` → `CWE-932` | confirmed — S045.txt L91–94; JSON path `$.content[5].children[2]`, parent `broken_access_control` (L73) |
| `authentication_bypass` → `CWE-287` | confirmed — L117–120; `$.content[6].children[0]` |
| `privilege_escalation` → `CWE-269` | confirmed — L97–100; `$.content[5].children[3]` |
| `metadata.default` null | confirmed — L2–4 |
| nodes without CWE carry `cwe: null` | **partial nuance** — 69 nodes carry explicit `"cwe": null`; 23 nodes (all non-leaf, all with children) carry **no `cwe` key at all**. Every leaf (184) carries a `cwe` key (62 null, 122 list). So the claim is true for 69 of 92 CWE-less nodes; `"cwe": null` literal occurs 69× in the snapshot. |

idor row verbatim (S045.txt L91–94):

```
"id": "idor",
"cwe": [
"CWE-932"
]
```

## 4. Determinism of plain-text `curl -sSL` fetch

Yes — deterministic for both, no JS: raw.githubusercontent serves the raw file bytes
(`text/plain; charset=utf-8`) with no scripted content; two independent fetches per URL were
byte-identical (sha256 stable), as was an instrument-UA fetch. The only nondeterminism source
is the upstream `master` ref moving; a commit-pinned URL
(`…/75f888a997a1cc307c62235d6b3325e53a215c60/README.md` and `/mappings/cwe/cwe.json`) returns
identical bytes (verified). Master HEAD at fetch time: `75f888a997a1cc307c62235d6b3325e53a215c60`
(2026-08-26T04:22:44Z). The blob sha1s above are the content-addressed pins inside that commit.

## 5. Instrument validation (source-recheck.py, scratch manifest — not the round manifest)

All candidate quotes validated in a scratch manifest (`.ufo/waves/round-29/wave1/scoutcap-scratch/`)
against the landed captures: S044 Q1–Q8 and S045 Q1–Q6 all `OK occurrences=1`; multi-line S045
quotes verified with anchors 91/117/97/2/7/11 (`anchor=N-ok`), exit 0. Control: `"cwe": null`
alone (11 normalized chars) is rejected `reason=quote-too-short-to-be-evidence`
(MIN_QUOTE_CHARS=12) — any entry quote must include the node id line.

## 6. Findings / defects observed in landed artifacts

1. **Wrong JSON paths in manifest `location` fields and in the entry.** The round-29
   `manifest.json` S045 Q1 location says `$.content[4].children[2]` — truth is
   `$.content[5].children[2]` (`content[4]` is `blockchain_infrastructure_misconfiguration`,
   which has no children). Q4 location says `$.content[5].children[7]` — truth is
   `$.content[6].children[8]` (`broken_authentication_and_session_management` child 8).
   The entry `corpus/knowledge/program-severity-ladders-and-reward-scales.md` repeats both in
   its `source:` header and letter. Per QUALITY Q9, `location` is documentation the instrument
   does not read — `source-recheck.py` still exits 0 — but the citations are factually wrong
   and the entry's falsifiable check 3 names the wrong paths. LabC2Probe also repeated the wrong
   `$.content[4].children[2]` in its findings.
2. **Entry inline quote not literal.** The entry quotes `"cwe": ["CWE-932"]` — that string
   occurs 0× in S045.txt (the capture stores it multi-line). The manifest's multi-line form
   matches (occ=1). Entry/paraphrase should note the structural rendering or quote the
   multi-line form.
3. **Minor line off-by-one.** Entry cites excessive_jwt_lifetime as "S045.txt:171"; node id is
   L170, `"cwe": null` is L171; manifest Q4 spans L170–171.
4. The staged merge claim "Nodes without a CWE carry `cwe: null`" is over-broad as noted in §3
   (23 non-leaf nodes have no key); the landed entry's wording ("individual nodes can have
   `"cwe": null`") is accurate.

## 7. Bounds compliance

Writes only under the lane repo: this receipt plus a scratch validation scratch
(`.ufo/waves/round-29/wave1/scoutcap-scratch/`, ~60 KB total — raw upstream bytes + landed
capture copies + means + recheck output; well under R14's few-hundred-KB tarball threshold).
No writes to fleet root, sibling lanes, git/jj state, `~/Projects/shokuknow`, templates, or
tool substrate. No pacman transaction; no tool installed (curl 8.23.0 present; capture-source.py
stdlib-only). No subagents/background jobs/labrat. No `agent://all` messages.
