== ExecCapS044 — round-29 wave-1 S044 capture receipt (Bugcrowd VRT README) ==
generated_utc=2026-10-25T18:16:42Z
claims_freeze=f28ff5d26b29270f93163117e7255e24f0b1d947
lane_base=7a6591c1eb8a14f427297980a96fa8bb339f29ee
answering_model=inception/mercury-3 (config route table; none passed by this seat)
files_changed=corpus/source-snapshots/round-29/S044.txt (capture; only)
tools_installed=none (no pacman/uv/npx transaction; host pacman pause respected; capture-source.py is stdlib-only)

== capture command (verbatim from item) ==
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-source.py --id S044 --url https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md --kind html --out corpus/source-snapshots/round-29/S044.txt

== result ==
S044 status=200 fetched_bytes=8881 snapshot_bytes=8187 sha256=8adfca615f3fc3ba9200c656a8184682b6de6d344d7436b74a7da11662b126bf utc=2026-10-25T18:16:18Z out=corpus/source-snapshots/round-29/S044.txt
exit=0
snapshot_lines=137 (plain-text fetch per instrument; HTML stripped, entities decoded, per-line whitespace collapsed)

== P1–P5 ladder label lines (verification) ==
Measured on the committed snapshot bytes (sha256 above), line-exact:
  line 34  - **P1**: Critical
  line 35  - **P2**: High
  line 36  - **P3**: Medium
  line 37  - **P4**: Low
  line 38  - **P5**: Informational
Assertion: bullet labels appear exactly once each, sequential P1→P5 at lines 34–38, label words exact — PASSED (regex `^-\s+\*\*P([1-5])\*\*:\s*(\w+)$`, 5 matches, no others).
Other textual `P\` occurrences (prose, not labels): P1 at lines 11, 33, 39; P4 at line 39; P5 at lines 11, 33 — all inside the two sentences below, no extra bullet.

== suggested-baseline override sentence (verification) ==
Line 11, exactly once (occurrence count = 1; plain-apostrophe-normalized variant count = 0 → single occurrence, no duplicate):
"It is important to remember that while the recommended priority, from P1 to P5 might apply without context, it'ss possible that application complexity, bounty brief restrictions or unusual impact could result in a different rating."
(as served by the raw source, the apostrophe in "it'ss" is U+2019 RIGHT SINGLE QUOTATION MARK; capture preserves it — the asserted quote includes the curly apostrophe)

== suggested-baseline scale sentence (supporting) ==
Line 33, exactly once:
"The priority represents Bugcrowd's suggested baseline technical severity of the vulnerability on a P1 (Critical) to P5 (Informational) scale."

== cross-check vs ScoutCapBugcrowd ==
ScoutCapBugcrowd confirmed (2026-10-25, independent fetch) the landed snapshot line numbers and occurrence counts exactly: L11 override sentence occ=1; L33 suggested-baseline scale sentence occ=1; L34-38 P1-P5 label block occ=1; CWE crosswalk mention at L127 (`- [CWE](mappings/cwe/cwe.json)`). Scout recon receipt: .ufo/waves/round-29/wave1/ScoutCapBugcrowd.md.

== notes / risks ==
- fetch bytes 8881 match the scout's predicted ~8881 B README; status 200.
- The capture pins the live master branch: this URL may serve different bytes later; the pinned sha256 and snapshot are the evidence of record. source-recheck assertions for S044 land in the round-29 manifest (other seat, C2).
- No PRE-STATE counter applies: this seat only produces the artifact, not a comparison column.
