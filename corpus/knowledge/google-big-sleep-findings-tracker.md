# Google Big Sleep public findings tracker — the Google Issue Tracker's own README for the tracker where Big Sleep's disclosed findings are collected: what the tracker is, the disclosure policies its findings follow, and the finding-record fields its issues carry

source: S092 — https://issuetracker.google.com/issues/430375499 — capture corpus/source-snapshots/round-59/S092.txt (6371 snapshot bytes = fetched bytes; sha256 048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38; recorded fetch 2026-11-03T21:37:55Z, HTTP 200; a same-sha probe open at 21:37:55Z and the recorded re-open at 21:38:47Z are byte-identical; an independent curl open of the same endpoint is parsed-structure-identical with transport-only byte differences, controls/s092-variance-check.txt; the capture is the tracker's own action JSON machine interface because the HTML pages serve an application shell, controls/s092-opens-r59.txt; the README body, the field definitions and the Impact enum all sit on capture line L2, located per quote below); manifest corpus/source-snapshots/round-59/manifest.json (10 assertions Q1-Q10, each occurrences=1 at its anchor)
verified-at: 2026-11-03 (opened this round; the tracker endpoint may vary transport encoding between responses — the digest pins the instant, and the 90d row recheck re-fetches and compares parsed structures and pinned quotes, never raw bytes)
ground: F40
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092   # run from any cwd (the cd prefix names the lane root); prints one sha256 OK + one Q-OK line per pinned quote with its occurrences= count and anchor note; exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote is absent from the capture, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

Google's Issue Tracker speaks for Google's own project: issue 430375499 ("[Big Sleep] README", S092.txt:2 Q1)
is the tracker's own README, kept in the tracker's Big Sleep component by the project it describes. Every
statement below is that README's first-party statement about its own tracker and its own handling commitments
(Q2 names the disclosure commitments, S092.txt:2 Q2). This entry records those statements and the finding-record
template the tracker serves; it does not verify any individual finding, does not count the tracker's issues (the
saved search's result set is not enumerable without the tracker's JavaScript application), and does not verify
the underlying research. It is documentation-only: it instructs no probing, scanning, login or submission against
any target, and carries no credential material.

## Claim 1 — the tracker is the collection point of Big Sleep's disclosed findings, and the short link in Project Zero's lead resolves to it

The tracker's own README names its subject: issue "[Big Sleep] README" (S092.txt:2 Q1) states "All issues
reported by the project so far can be found [here](https://goo.gle/bigsleep)" (S092.txt:2 Q3). The recorded
Leads bullet on the tracker (corpus/SOURCES.md, Big Sleep bullet, bytes unchanged this round) resolves: the opens
receipt records `https://goo.gle/bigsleep` returning HTTP 200 at final URL
`https://issuetracker.google.com/savedsearches/7155917`, the tracker's saved search for the project
(.ufo/waves/round-59/controls/s092-opens-r59.txt). Falsifiable rule: a Big Sleep disclosed-finding list served
anywhere other than this tracker's saved search, or a README "found here" link resolving elsewhere, contradicts
the README as served on the recorded fetch date. Rejected over-generalization: the README grants no intake —
nothing in it invites researchers to file their own findings into this tracker, and Google's researcher-intake
surfaces stay the bug-hunters ground (S072) and the Google Cloud VRP rules (S069, F26), not this README.

## Claim 2 — the tracker's findings follow Google's disclosure policy and Project Zero's 2025 policy and disclosure trial

The README's commitment sentence is: "Findings from the project will be publicly disclosed following [Google's
industry standard disclosure policy]" (S092.txt:2 Q2), and it names Project Zero's 2025 policy and disclosure trial
at https://googleprojectzero.blogspot.com/2025/07/reporting-transparency.html (S092.txt:2). The trial itself is
held ground: corpus/knowledge/pz-reporting-transparency-trial.md (source S017) already records that Big Sleep joins
the Project Zero trial (S017.txt L28). What this entry adds is the tracker's own statement that binds Big Sleep's
published findings to both named policies. Falsifiable rule: a Big Sleep finding disclosed outside the process
those two named policies define, or a third policy the README does not name being cited as the project's disclosure
rule, contradicts the README as served. Rejected over-generalization: the sentence is the tracker's own commitment
about its own project; it is not a disclosure deadline (no interval appears in the README) and does not modify the
policies it names.

## Claim 3 — the tracker's finding-record template carries Product, Reported and Fixed fields and a four-value Impact enum

The capture serves the tracker's field definitions beside the README: "Impact of the vulnerability" (S092.txt:2 Q4)
with the value list ["High","Medium","Low","None"] (S092.txt:2 Q7), "Software product the vulnerability was found in"
(S092.txt:2 Q5), "Date when the bug was reported" (S092.txt:2 Q6) and "Date when the bug was fixed" (S092.txt:2 Q8).
This is the per-finding metadata contract the tracker itself serves for Big Sleep reports. Falsifiable rule: a Big
Sleep tracker issue whose served template carries an Impact value outside the four-value enum, or that lacks the
named fields, contradicts the template as served on the recorded fetch date. Rejected over-generalization: the
four-value Impact is the tracker's coarse triage field, not a severity system — it is not CVSS (F01), not a
program's severity ladder (F13), not Immunefi's VSCS (F17), and it defines no reward.

## Claim 4 — the README dates the tracker's example issue and states the project's Naptime lineage

The issue record's Reported value is "2025-07-08" (S092.txt:2 Q9), and the README's further-reading list opens with
"[Project Naptime: Evaluating Offensive Security Capabilities of Large Language Models]" (S092.txt:2 Q10), linking
https://googleprojectzero.blogspot.com/2024/06/project-naptime.html beside
https://googleprojectzero.blogspot.com/2024/10/from-naptime-to-big-sleep.html (S092.txt:2) — the documents S010
already mines (F04). Falsifiable rule: a lineage claim that derives Big Sleep from a project other than the Naptime
work the README itself links, or a README authored before the tracker existed, contradicts the capture. Rejected
over-generalization: the date and links date the tracker's example issue and its reading list, not the project's
start; nothing in the capture states when Big Sleep itself began.

## Limits

- The admitting read is the tracker's own action JSON machine interface (capture_url in the manifest); the HTML pages
  (issues/430375499, savedsearches/7155917) serve an SPA application shell to the lane instrument, recorded in
  .ufo/waves/round-59/controls/s092-opens-r59.txt. The saved search's result set is therefore not enumerated anywhere
  in this entry: no issue count, no issue contents, no per-finding Impact values are asserted.
- The endpoint varies transport encoding between responses (CRLF and serialization spacing); the two opens this
  round are parsed-structure-identical (.ufo/waves/round-59/controls/s092-variance-check.txt). The manifest sha256
  pins the instant, per the S069 precedent; the recheck compares pinned quotes and digests, never raw bytes across
  time.
- All ten pinned quotes sit on capture line L2 (the single JSON body line); the anchor-referent table in
  corpus/lessons/round-59.md § Gate maps each cited line to the sentence it supports (R71).
- Held-ground overlap: the Project Zero trial and Big Sleep's participation in it are S017's ground
  (corpus/knowledge/pz-reporting-transparency-trial.md); this entry holds the tracker README's own statements only,
  and the AI-assisted-finding-validation method stays F04 (S009-S012).
