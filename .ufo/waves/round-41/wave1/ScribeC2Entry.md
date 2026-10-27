# ScribeC2Entry — round 41 wave 1 receipt (C2 coverage: F24 RFC 9116 + S063 + knowledge entry)

Seat: `ScribeC2Entry` (leaf, no subagent dispatch). Item: deliver the byte-exact knowledge entry
`corpus/knowledge/rfc-9116-security-txt.md` for new registry row S063 / frontier F24, with the
provenance trio, section-anchored claims and `<<<CAPTURE:Lnnn>>>` line placeholders the L1 splices
after `ExecC2Capture` lands the capture.

Deliverable (byte-exact, beside this receipt):
`.ufo/waves/round-41/wave1/ScribeC2Entry.entry.md` — 53 lines, 11,179 bytes,
sha256 `a3a52323f53d5823e2fe4845922b0bf23c56f6a98534786d228ef3a1e248bbf6`
(copied with `cp`; re-hashed at the destination: same digest; no trailing whitespace,
`grep -cE ' +$'` → 0; no BOM, first bytes `23 20 52 46`; final byte `\n`). The L1 copies it to
`corpus/knowledge/rfc-9116-security-txt.md` unchanged; the only edits that may legitimately follow
are the placeholder splices in §1.

## 1. Placeholder splice contract

Two kinds of marker, both must be spliced before the entry is admissible:

1. `<<<CAPTURE>>>` ×3, all on the `source:` line, in the order `(lines, bytes; sha256)`.
2. `<<<CAPTURE:Lnnn>>>` ×21 — one per verbatim quote, with the two §2.5.4 quotes of entry line 17
   sharing a line. They appear in **strictly ascending capture-line order**, so a mechanical splice
   of the k-th marker with the k-th line in §5 reproduces the entry exactly. Verified mechanically:
   `ascending=True`; every anchored line carries exactly as many markers as quoted spans.

Splice values, measured on the bytes that will be the capture (§4.1 shows they are byte-identical to
`ExecC2Capture`'s snapshot):

```
<<<CAPTURE>>>  →  842 lines, 39,301 bytes; sha256 925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa
```

If the landed capture ends up with another digest, do not reuse these line numbers: re-derive the 21
anchors with the command in §4.2, or splice by quote text. The entry's `recheck:` line fails closed
on any digest it does not recognise (`S063:sha256 MISMATCH`, exit 1), so a wrong splice cannot pass.

**Attribution convention (fixed after the L1's harness finding).** Every one of the 19 marker lines
reads `— S063.txt:L<<<CAPTURE:Lnnn>>> (§x)`, not `— §x, L<<<CAPTURE:Lnnn>>>`. `frontier-recheck-count.py`
builds `cited_ids` only from `S\d{3,}` tokens on lines that are **not** the `source:` or `recheck:`
line, so a section-only attribution left `S063` cited nowhere and the row failed with
`selection-not-cited-by-entry` (the L1's `entries=27 pass=26`). With the convention above the entry
mentions `S063` on 19 lines outside the declaration lines; §4.8 reproduces the harness verdict both
ways on identical fixtures.


## 2. What I read (and its digest)

| path | sha256 | use |
|---|---|---|
| `corpus/knowledge/cyclonedx-analysis-subtree.md` | `5a549e312237372a639931cc980ea697f60d383999790b9d48d5df4bd5d1978c` | model entry A (322 lines): trio order, `ground:` line, `# prints … exits …` recheck note, FC/limit sections |
| `corpus/knowledge/cisa-when-to-issue-vex.md` | `5010a107cc7ef34bcd7e8d1a74eb2a2bb2a71c3ea666577506d7c2f93dc25d29` | model entry B (144 lines): same trio, same `--manifest … --source S0xx` recheck family, rejected-over-generalization style |
| `corpus/QUALITY.md` (base `5b29ea14`) | — | admission bar Q1–Q10, R12 (recheck `--source` coverage) |
| `corpus/instruments/source-recheck.py` (base) | — | what the `recheck:` line must be, and how quotes/anchors are judged: B1 stem=id, B2 non-unique quote needs a verifying anchor, `quote-too-short-to-be-evidence`, whitespace collapse |
| `corpus/instruments/frontier-recheck-count.py` (base) | — | rule A (declared `source:` ids == `--source` ids, both directions), rule C (must be `source-recheck.py --manifest … --source …`) |
| `corpus/instruments/recheck-audit.py` (base) | — | strict limbs `parse/cwd/paths/cdroot/instrument/own`; `own` is satisfied by `--source` + `corpus/source-snapshots/` |
| `corpus/knowledge/policy-access-playbook.md:12`, `SKILL.md:131` | — | the lane's pre-existing RFC-9116 stub rows; not edited by me and not contradicted by this entry (they record a round-15 routing stub, not ground) |
| `.ufo/waves/round-41/wave1/ScoutRfc9116.facts.txt` | — | sibling scout strip: same source, raw-line map, and the "RFC 9116 is not admitted ground yet" coverage check |
| `/fast/scratch/hyaku/kasegi-r41/ExecC2Capture/S063.instrument.txt` (peer scratch, read-only) | `925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa` | the capture bytes and their normalization, confirmed by the peer's IRC message |

Reading of the two model entries, as the item asked: both open directly under the H1 with `source:` /
`verified-at:` / (`ground:`) / `recheck:`; both put the capture path inside the `source:` line with
line count, byte count and digest; both make `recheck:` one `cd <lane-root> && python3
corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-NN/manifest.json
--source S0xx   # …` command whose `#` note names the fail-closed exits; both close with a
rejected-over-generalization list and an honest limit. My entry keeps the trio, the `ground:` line
and the recheck family, and meets the item's 55-line bar at 53 lines: it folds the rejected
over-generalizations into Claim 7's prose and the falsifiable-rule block, and states the honest
limit as one paragraph.

## 3. Network fetch (mine)

```
2026-10-27T08:18:54Z  curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 \
  https://www.rfc-editor.org/rfc/rfc9116.txt
http=200 bytes=45129 url=https://www.rfc-editor.org/rfc/rfc9116.txt
sha256 79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9
wc -l → 1122
```

I fetched nothing else until a verification re-fetch at the end of the seat
(`2026-10-27T08:33:41Z`, same URL, HTTP 200, 45,129 bytes, sha256 `79d19ce7…`), whose
`capture-source.py --kind text` collapse again gave 842 lines / 39,301 bytes / `925512e7…` — the
normalization is reproducible across three separate fetches (mine twice, the peer's once), and all
three agree on the served body's digest. The peer's fetch was `2026-10-27T08:19:23Z`, 45,129 bytes,
same digest. The re-fetch was used only for the span check in §4.7 and its scratch was deleted.

## 4. Validation actually run (scratch only, nothing written into the lane corpus)

Scratch: `S=/fast/scratch/hyaku/kasegi-r41/ScribeC2Entry` (removed before yield). Disk guard read
first: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → green
(`/tmp` 3%, `/var/tmp` 35%, `/fast/scratch/hyaku` 25%).

**4.1 Bytes.** I reproduced the lane's own normalization (`capture-source.py --kind text`
`collapse()`) from my fetch: 842 lines, 39,301 bytes, sha256
`925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa`.
`cmp` against `ExecC2Capture`'s `S063.instrument.txt` → identical; `sha256sum` of both → the same
digest. That file has no slice marker, and the peer reports the capture is the whole document with
line 1 being the BOM alone, so the entry cites text from L104 onward only.

**4.2 Quotes: verbatim, ≤25 words, exactly once, ascending.** Measured on the capture bytes
(`landed-shape.txt` = that byte-identical file), with the raw 1,122-line fetch as a second,
independent check:

- capture bytes: 21/21 spans `occ=1`, max words **25** (row 16, the §3.1 sentence), anchors
  ascending `104 < 115 < 189 < 227 < 235 < 249 < 250 < 254 < 266 < 270 < 273 < 281 < 330 < 333 <
  335 < 349 < 357 < 528 < 536 < 538 < 571`;
- raw bytes: the same 21 spans are `occ=1` with anchors `126, 139, 237, 290, 299, 317, 318, 323,
  343, 347, 351, 365, 439, 442, 444, 462, 472, 716, 726, 728, 768`.

Anchor re-derivation command (run it against whatever file the capture lands as):

```sh
cd /fast/scratch/hyaku/kasegi-r41/ScribeC2Entry && python3 - <<'PY'
import re,bisect
raw=open('capture.txt',encoding='utf-8').read()          # ← the landed S063.txt
norm=lambda t:" ".join(re.sub(r"</?u>","",t).split())
toks=[]; nl=[m.start() for m in re.finditer('\n',raw)]
for m in re.finditer(r'\S+',raw): toks.append((m.group(0),bisect.bisect_right(nl,m.start())+1))
ntext=" ".join(t for t,_ in toks); starts=[]; p=0
for t,_ in toks: starts.append(p); p+=len(t)+1
for l in open('entry.md',encoding='utf-8'):
    if '<<<CAPTURE:Lnnn>>>' not in l: continue
    for m in re.finditer(r'"((?:[^"\\]|\\.)*)"',l):
        q=norm(m.group(1).replace('\\"','"')); o=re.search(re.escape(q),ntext).start()
        print(ntext.count(q), toks[bisect.bisect_right(starts,o)-1][1], q[:60])
PY
```

**4.3 The entry's `recheck:` line as landed text.** `bash -n` → rc 0 (one command, note after `#`);
starts `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`; carries `--manifest
corpus/source-snapshots/round-41/manifest.json --source S063`. Run today it is fail-closed exactly as
its note says: `bash -c "$line"` from the lane root → exit **2**, output
`manifest UNAVAILABLE reason=missing` (the round-41 snapshot dir does not exist:
`ls corpus/source-snapshots/round-41` → exit 2). Harness limbs checked statically: rule A —
`source: S063` is the only declared id and `--source S063` the only selection; rule C — it is a
`source-recheck.py` invocation with `--manifest` and `--source`; audit `own` limb — the line carries
`--source` and `corpus/source-snapshots/`, so it is bound to its own entry; `paths` limb — both named
corpus paths will exist once the manifest lands.

**4.4 Positive run (simulation in scratch over the capture bytes, not a landed run).** Scratch
mirror `fxL/` holding the real `source-recheck.py`, `S063.txt` = the byte-identical capture, and a
manifest pinning the entry's 21 quotes with the §5 anchors:

```
cd fxL && python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-41/manifest.json --source S063
positive_exit=0 ; quote_ok_lines=21 ; mismatch=0
```

**4.5 Controls — four mutations of the capture, each isolating one limb.** Digest re-pinned in every
control except A, so only the intended limb can fire:

| control | mutation of the capture bytes | result |
|---|---|---|
| A | one bit flipped at byte 20000 | `S063:sha256 MISMATCH expected=925512e7… actual=968215c6…`, exit **1** |
| B | line 536 `Not having` → `Not keeping` (Q19's sentence destroyed) | `S063:Q19 MISMATCH reason=quote-not-found`, exit **1** |
| C | truncated to its first 400 lines (a slice): claims would read past the capture | 4 × `MISMATCH reason=quote-not-found` (Q18–Q21), exit **1** |
| D | Q19's sentence duplicated verbatim on line 400 (occurrences=2) | `S063:Q19 OK occurrences=2 anchor=536-ok`, exit **0** — the anchor limb is what keeps a duplicated quote pinned to its declared line, the Q9 rule |

A/B/C are the fail-closed limbs; D is a pass control that shows the anchor, not substring presence,
is doing the binding.

**4.6 The peer's own manifest, read-only.** `ExecC2Capture`'s scratch record
(`/fast/scratch/hyaku/kasegi-r41/ExecC2Capture/recheck-round41/manifest.json`) pins 3 quotes at
anchors 330, 270, 235 and passes: `S063:sha256 OK`, `Q1 anchor=330-ok`, `Q2 anchor=270-ok`,
`Q3 anchor=235-ok`, exit 0. All three anchors equal mine for the same sentences.

**4.7 Every quoted span in the entry, not just the 21 anchored ones.** Two independent checks agree:

- the peer (`ExecC2Capture`, by IRC, verified against the capture bytes) located 33 spans —
  "33 spans, 0 unlocated, 0 non-unique";
- I re-verified the same thing first-hand against a second fetch collapsed to the capture
  (`§3`): 33 quoted spans ≥4 words, **0** with `occurrences != 1`, max 25 words, every one located,
  capture lines `104, 115, 169 (×2), 182, 184, 189, 227, 235, 249 (×2), 250, 254, 256, 266, 267, 270,
  273, 281, 330, 333, 335, 339, 340, 349, 350, 357, 358, 528, 536, 538, 571, 573` — identical to the
  peer's list. 21 of the 33 carry `<<<CAPTURE:Lnnn>>>`; the other 12 are inline quotations supported
  by their section anchors (§1.1/§2.3/§2.4/§2.5.4/§2.5.5/§3/§3.1/§5.3/§5.5), so no quoted span in
  the entry is unlocated.

The peer's two cautions are met: capture line 1 is the BOM alone, and no claim or quote here reads
L1 (lowest anchored line is L104); and the stray `349/457→357` token was a typo in my IRC ack only —
`grep -c 457` on both delivered files → `0` for each, and the §5 table carries 349 and 357.

**4.8 Harness verdict, both ways, on identical fixtures (the L1's fix A).** Scratch fixture lanes
(`fx/` = this entry, `fxold/` = the pre-fix attribution style) each hold a `corpus/README.md` Frontier
row `| F24 | … | admitted | knowledge/rfc-9116-security-txt.md | S063 |`, the entry at
`corpus/knowledge/rfc-9116-security-txt.md`, the real `source-recheck.py`, the capture and a manifest
pinning the 21 quotes. The only difference between the two lanes is the attribution text. In each
fixture copy the recheck line's `cd` was rewritten to that fixture root (the delivered entry keeps the
lane path); nothing else changed.

```
python3 corpus/instruments/frontier-recheck-count.py --root fx
PASS     F24  knowledge/rfc-9116-security-txt.md   ids=S063   exit=0
entries=1 pass=1 exit=0                                         # rc 0

python3 corpus/instruments/frontier-recheck-count.py --root fxold        # pre-fix attributions
FAIL     F24  knowledge/rfc-9116-security-txt.md   ids=S063   exit=-   problems=selection-not-cited-by-entry
entries=1 pass=0 exit=1                                         # rc 1
```

So the fix is measured, not assumed: the same entry, the same capture, the same pins, and the citation
limb is the only thing that moves. On the integrated tree the row should print `PASS F24 … ids=S063`
as above (`entries=27 pass=27` once the other 26 rows are unchanged).

## 5. Quote pin table (ordinal = marker order in the entry; capture line = landed normalization)

| # | entry line | capture line | §  | words | quote (verbatim) |
|---|---|---|---|---|---|
| 1 | 8 | 104 | 1.1 | 12 | Other details of vulnerability disclosure are outside the scope of this document |
| 2 | 8 | 115 | 1.1 | 18 | The "security.txt" file is intended to be complementary and not a substitute or replacement for other public resources |
| 3 | 11 | 189 | 2.5 | 9 | Unless otherwise stated, all fields MUST be considered optional. |
| 4 | 12 | 227 | 2.5.3 | 10 | This field MUST always be present in a "security.txt" file. |
| 5 | 16 | 235 | 2.5.3 | 17 | When the value of this field is an email address, it is RECOMMENDED that encryption be used |
| 6 | 17 | 249 | 2.5.4 | 7 | Keys MUST NOT appear in this field. |
| 7 | 17 | 250 | 2.5.4 | 19 | the value of this field MUST be a URI pointing to a location where the key can be retrieved |
| 8 | 18 | 254 | 2.5.4 | 19 | it is always the security researcher's responsibility to make sure the key being specified is indeed one they trust |
| 9 | 22 | 266 | 2.5.5 | 22 | indicates the date and time after which the data contained in the "security.txt" file is considered stale and should not be used |
| 10 | 23 | 270 | 2.5.5 | 20 | It is RECOMMENDED that the value of this field be less than a year into the future to avoid staleness. |
| 11 | 24 | 273 | 2.5.5 | 13 | This field MUST always be present and MUST NOT appear more than once. |
| 12 | 28 | 281 | 2.5.7 | 14 | The "Policy" field indicates a link to where the vulnerability disclosure policy is located. |
| 13 | 29 | 330 | 3 | 10 | organizations MUST place the "security.txt" file under the "/.well-known/" path |
| 14 | 30 | 333 | 3 | 15 | For legacy compatibility, a "security.txt" file might be placed at the top-level path or redirect |
| 15 | 31 | 335 | 3 | 18 | If a "security.txt" file is present in both locations, the one in the "/.well-known/" path MUST be used. |
| 16 | 35 | 349 | 3.1 | 25 | A "security.txt" file MUST only apply to the domain or IP address in the URI used to retrieve it, not to any of its subdomains |
| 17 | 36 | 357 | 3.1 | 17 | Organizations SHOULD use the policy directive (as per Section 2.5.7) to provide additional details regarding the scope |
| 18 | 40 | 528 | 5.2 | 20 | researchers should record any redirects since they can lead to a different domain or IP address controlled by an attacker |
| 19 | 41 | 536 | 5.3 | 15 | Not having a "security.txt" file may be preferable to having stale information in this file. |
| 20 | 42 | 538 | 5.3 | 23 | Organizations must use the "Expires" field (see Section 2.5.5) to indicate to researchers when the data in the file is no longer valid. |
| 21 | 46 | 571 | 5.5 | 19 | researchers shouldn't assume that the presence or absence of a "security.txt" file grants or denies permission for security testing |

Cross-checks: the peer's section map (IRC, item 3) has §3 heading L329 / body L330, §3.1 L348, §2.5.5
L265, §5.2 L526, §5.3 L532, §5.5 L559 — every anchor above falls inside the right section; the
sibling scout's raw-line ranges (`ScoutRfc9116.facts.txt` §3, §4, §6) agree with the raw-line column
in §4.2. No quote was invented: all 21 are substrings of the capture under whitespace collapse.

Alignment with the peer's corrections (IRC item 4), which the item brief's guesses got wrong: the
entry puts `Expires` in §2.5.5 and states the one-year bound as RECOMMENDED (row 10) with the
separate REQUIRED/single rule (row 11); `Encryption` is §2.5.4 (rows 6–8) while §2.3 is Digital
Signature (cited in Claim 2's prose); the encryption RECOMMENDATION is attributed to §2.5.3 (row 5).
`CSAF` appears nowhere in the entry, per the peer's `grep -c` of the capture (0). I do not cite the
L383 ABNF-comment "Section 3.5.3" defect (errata 6946): the entry makes no claim about that comment.

## 6. QUALITY compliance (the parts this seat controls)

| id | how the entry meets it |
|---|---|
| Q1 | lines 3–5 directly under the H1: `source: S063 — URL — capture corpus/source-snapshots/round-41/S063.txt (lines, bytes; sha256)` + `verified-at: 2026-10-27` + one-command `recheck:`; `ground: F24` on line 6 |
| Q2 | one tier-A row (IETF RFC 9116), opened this round; no tier-C support anywhere |
| Q3 | 33 verbatim spans, ≤25 words each (max 25): 21 carry a capture line (§5), the other 12 are inline with their § anchors; all 33 measured exactly-once, §4.7 |
| Q4 | attributed to the RFC and its authors; line 8 says "never a claim about any named organization's practice"; Informational status stated in the entry and in the honest limit |
| Q5 | `**Falsifiable rule.**` with six checkable limbs (a)–(f); two rejected over-generalizations with §5.5 as the reason (Claim 7) |
| Q6 | documentation only: no probing/scanning/logging-in/submitting instruction, no credential, session or private URL; the capture is public RFC text |
| Q7 | `recheck:` is a command; its output names what it checked (per-quote `occurrences=`/`anchor=`); the missing-manifest control was run (§4.3, exit 2) |
| Q8 | the entry quotes plain text only, no converter markup; where a quote spans a line break the instrument reports `normalized=markup-whitespace`, which is its own declared transformation |
| Q9 | every span is exactly-once **and** carries an anchor (§5); control D shows the anchor is what holds when a duplicate appears |
| Q10 | one line, `bash -n` rc 0, `cd <lane-root> &&` prefix, human note after `#` |
| R12 | `--source S063` equals the entry's only declared id; the named manifest must list S063 (it will) |

## 7. What the L1 still has to land around this entry

1. `corpus/source-snapshots/round-41/S063.txt` (842 lines / 39,301 bytes /
   `925512e7…`) plus `manifest.json` from `ExecC2Capture`'s record (`{id: S063, path: S063.txt,
   url, fetched_utc, status: 200, size_bytes/snapshot_bytes, lines, sha256, quotes[]}`). `path` stem
   must equal the id or the instrument prints `reason=stem-mismatch`.
2. **Decide whether to extend that record's `quotes[]` beyond its three Gate pins.** The peer states
   its item fixes the record at exactly Q1/Q2/Q3 (anchors 330, 270, 235) and that it did not widen it
   silently; it also supplies a verified 33-span list. The record passes as-is (exit 0), but it binds
   3 of the entry's 21 anchored assertions; §5 holds the 21-pin table the entry needs if the L1 wants
   its own claims pinned rather than three of them.
3. The `source:` splice values in §1.
4. `corpus/SOURCES.md` row S063 (kind spec, tier A, status mined, opened 2026-10-27) and the
   `corpus/README.md` F24 row whose entry cell resolves to this file (a row with a missing entry
   path fails the harness with a named-row `missing-entry`), plus the `PROVINCE.md` F24 amendment.
5. `corpus/instruments/knowledge-expected.txt` must gain `corpus/knowledge/rfc-9116-security-txt.md`,
   or `recheck-audit.py` prints `unexpected=` and the audit fails.
6. Nothing else of mine needs cascading: I edited no existing lane file, added nothing under
   `corpus/knowledge/`, and left the round-15 RFC-9116 stub rows (`policy-access-playbook.md:12`,
   `SKILL.md:131`) untouched — they describe a routing stub, not ground, and the L1 may retire or
   keep them without changing this entry.

## 8. Limits of this seat's evidence

- My runs in §4.4–4.5 are **scratch simulations over the capture bytes**, not runs on the landed
  path: they prove the entry's quotes, anchors and failure paths behave as claimed on those exact
  bytes, and they do not substitute for the post-landing run the L1 makes. The entry's `recheck:`
  stays exit 2 until the manifest exists — measured, §4.3.
- The capture itself is `ExecC2Capture`'s artifact (peer scratch, read-only here): 842 lines /
  39,301 bytes / `925512e7…`, byte-identical to my own normalization of my own fetch (`cmp` clean).
  If the L1 lands different bytes, §1's numbers and §5's line column are stale and must be
  re-derived, which is why the recheck pins a digest.
- Entity claims about vendor practice are deliberately absent: the RFC defines a format; the entry
  says so instead of asserting who publishes a `security.txt` today.
- No tool installs or upgrades were needed (none recorded), no `pacman`, no mutating git/jj, no
  writes outside `.ufo/waves/round-41/wave1/ScribeC2Entry.*` and
  `/fast/scratch/hyaku/kasegi-r41/ScribeC2Entry/`. Scratch removed before yield.
