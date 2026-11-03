VERIFIED — S089: verified; S090: verified. Both committed snapshots reproduce byte-for-byte from fresh opens through the committed instrument's `html_to_text`, every manifest pin matches, all 14 manifest quotes sit exactly once at their pinned anchor lines, every quote is ≤ 25 words (max 22), and both SOURCES.md rows are `mined` with no rejected cell.

Seat: ReopenSources, round-57 w1. Target: non-author verification of the S089 and S090 captures (C2 sourced rows). All paths absolute; lane L = /home/vgpnk/Projects/shokunin/kasegi-shokunin (read-only throughout); scratch S = /fast/scratch/hyaku/kasegi-r57/ReopenSources (TMPDIR=S; deleted before yield, item 8).

## 0. Tooling authorization record (RULES.md, operator 2026-10-19)
Read /home/vgpnk/.omp/agent/RULES.md before starting. No tool installed or upgraded: every needed tool was already present (all preexisting system tools, no channel used, pacman untouched per the host-wide pause). Versions as printed on this host: curl 8.23.0 (x86_64-pc-linux-gnu), python3 3.14.8, grep (pi-uu-grep) 0.2.0, sha256sum 0.8.0, GNU-less coreutils print — the same tools the lane's own instruments invoke.

## 1. Committed digests vs manifest pins (seat step 1)
Command:
    cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/source-snapshots/round-57/S089.txt corpus/source-snapshots/round-57/S090.txt && wc -c corpus/source-snapshots/round-57/S089.txt corpus/source-snapshots/round-57/S090.txt && wc -l corpus/source-snapshots/round-57/S089.txt corpus/source-snapshots/round-57/S090.txt
Output (exit=0):
    17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd  corpus/source-snapshots/round-57/S089.txt
    2074d3a1b89fe858e607db8cb6109ee869932a12ea14050ad4276084a6c2976a  corpus/source-snapshots/round-57/S090.txt
    6647 corpus/source-snapshots/round-57/S089.txt
    5598 corpus/source-snapshots/round-57/S090.txt
    268 S089.txt / 261 S090.txt lines
Comparison against the manifest sha256 fields read with python3 json (driver in item 3, `json.load` of L/corpus/source-snapshots/round-57/manifest.json; fields at manifest lines 24 and 52):
    S089 manifest_pin_sha256=17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd pin_match=True
    S090 manifest_pin_sha256=2074d3a1b89fe858e607db8cb6109ee869932a12ea14050ad4276084a6c2976a pin_match=True
Both pins also equal the C2 kill-rule digests in .ufo/waves/round-57/claims.json (read, not modified). `snapshot_bytes` 6647/5598 and `lines` 268/261 match manifest fields exactly.

## 2. Fresh open, this seat, 2026-11-03 (seat step 2a)
Commands (verifier UA, distinct from the capture UA — an independent re-open, not a replay):
    curl -sS -L --max-time 60 -A 'kasegi-research-verifier/1.0 (independent re-open; contact: operator)' -o $S/S089.html -w 'S089 http=%{http_code} bytes=%{size_download} final=%{url_effective}\n' https://www.iso.org/standard/72311.html
    curl -sS -L --max-time 60 -A 'kasegi-research-verifier/1.0 (independent re-open; contact: operator)' -o $S/S090.html -w 'S090 http=%{http_code} bytes=%{size_download} final=%{url_effective}\n' https://www.iso.org/standard/69725.html
Output (exit=0):
    S089 http=200 bytes=88964 final=https://www.iso.org/standard/72311.html
    S090 http=200 bytes=87845 final=https://www.iso.org/standard/69725.html
The raw fetched byte counts equal the manifest `bytes` fields (88964 / 87845, manifest lines 25 and 53): the same content volume is served today as at capture time.

## 3. Conversion reproduction through the committed instrument (seat step 2b)
Driver: $S/convert_check.py (scratch, deleted with S; decisive logic below — read-only import, no lane mutation):
    spec = importlib.util.spec_from_file_location("capture_source_ro", L + "/corpus/instruments/capture-source.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    raw = open(S + "/" + sid + ".html", "rb").read()
    text = mod.html_to_text(raw.decode("utf-8", "replace"))   # capture()'s exact call shape (capture-source.py:81)
    data = text.encode("utf-8")                                # written to $S/<sid>.rec.txt
    fresh = hashlib.sha256(data).hexdigest(); committed = sha256 of the L snapshot bytes
Run: `TMPDIR=$S python3 $S/convert_check.py` → exit=0, no differing lines:
    S089 fresh_open_sha256=17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd fresh_bytes=6647 committed_bytes=6647 fresh_eq_committed=True
    S090 fresh_open_sha256=2074d3a1b89fe858e607db8cb6109ee869932a12ea14050ad4276084a6c2976a fresh_bytes=5598 committed_bytes=5598 fresh_eq_committed=True
Fresh-open conversion is byte-identical to the committed snapshots; the first-differing-line branch never fired. Bytes reproduce from a fresh open for both sources.

## 4. Per-quote anchor and uniqueness (seat step 3)
Method: every manifest quote extracted verbatim by JSON decode (never retyped; unicode em-dash and apostrophe preserved) into one file per quote — driver `$S/extract_quotes.py`, 14 files under $S/q/, plus $S/quotes.tsv (source, quote id, anchor, path). Loop `$S/quotecheck.sh` then ran, per quote: `Q="$(cat $qfile)"`, `grep -n -F -- "$Q" $snap` (hit line must equal the manifest anchor), `grep -c -F -- "$Q" $snap` (must print 1). Output (exit=0):
    S089 Q1 anchor=1 hit=1 count=1 OK
    S089 Q2 anchor=84 hit=84 count=1 OK
    S089 Q3 anchor=91 hit=91 count=1 OK
    S089 Q4 anchor=92 hit=92 count=1 OK
    S089 Q5 anchor=99 hit=99 count=1 OK
    S089 Q6 anchor=64 hit=64 count=1 OK
    S089 Q7 anchor=204 hit=204 count=1 OK
    S090 Q1 anchor=1 hit=1 count=1 OK
    S090 Q2 anchor=84 hit=84 count=1 OK
    S090 Q3 anchor=85 hit=85 count=1 OK
    S090 Q4 anchor=92 hit=92 count=1 OK
    S090 Q5 anchor=64 hit=64 count=1 OK
    S090 Q6 anchor=197 hit=197 count=1 OK
    S090 Q7 anchor=109 hit=109 count=1 OK
Snapshots: L/corpus/source-snapshots/round-57/S089.txt (anchors 1, 84, 91, 92, 99, 64, 204), S090.txt (anchors 1, 84, 85, 92, 64, 197, 109). 7 quotes per source, matching the manifest `quotes` arrays (manifest lines 26-60 and 54-88) and the C2 expectation of 7 Q lines each.

## 5. Quote word counts (seat step 4)
`wc -w < $S/q/<file>` per quote (same loop; counts agree with the JSON-side `len(quote.split())` cross-check):
    S089 Q1=11 Q2=17 Q3=17 Q4=22 Q5=6 Q6=9 Q7=3   (max 22)
    S090 Q1=12 Q2=20 Q3=10 Q4=6 Q5=9 Q6=3 Q7=7   (max 20)
Quotes over 25 words: none (0 of 14).

## 6. Registry hygiene — no rejected row this round (seat step 5)
Command:
    grep -n -E '^\| S08[89]|^\| S090' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
Output (exit=0): exactly two new rows — corpus/SOURCES.md:96 (S089) and :97 (S090); :95 is the pre-existing S088 row matched by the S08[89] pattern, unchanged context. Full-row read of :96-:97: both rows are kind `docs`, tier `A`, carry the capture cell pinning this item's snapshot path and the same sha256 values verified in items 1/3, status cell `mined`, date 2026-11-03, knowledge target corpus/knowledge/iso-29147-30111-standard-records.md — no `rejected` cell in either row. The row cell's anchor list (S089: title L1, abstract scope L84, cross-reference L91, applicability L92, stage L99, currency L64, successor AWI L204; S090: title L1, abstract L84, applicability L85, stage L92, currency L64, successor WD 30111.2 L197, review cadence L109) matches the manifest anchors verified in item 4 line-for-line.

## 7. Notes for the claim owners (observations only; nothing edited)
- Strength, not a defect: this re-open succeeded with a different User-Agent than the capture (verifier UA vs the instrument's UA string disclosed in manifest.json:5-6 and the `fetch_method` cells), and still reproduced identical bytes — the content is stable across UA variants, which hardens C2's sha kill-rule pins against a UA-dependent server behavior explanation.
- The instrument's own urllib open was NOT re-attempted by this seat (the manifest and claims.json host-facts disclose the HTTP-403 on www.iso.org; the seat spec prescribes curl). The 403 claim is therefore taken as disclosed, not independently reproduced — no evidence gap for this seat's target, which is capture reproduction, not the fetch-path disclosure.

## 8. Scratch cleanup
`rm -rf -- /fast/scratch/hyaku/kasegi-r57/ReopenSources` run before yielding (see transcript); leftover check printed nothing — no leftovers to name. Evidence file path: /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-57/w1/ReopenSources.md (this file). Lane untouched except this file; claims.json, manifest.json, SOURCES.md, snapshots, and instruments read-only.

Report: .ufo/waves/round-57/w1/ReopenSources.md
