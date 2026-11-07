history.tsv columns: commit, date, hits, files, allowed, unused_allow, scanned, rc, lines
- commit: full SHA, 34 commits from 4ab545865f747fca8456370b5927fe51236fe579 (round-80 freeze) to 132e16c588a2424c06b5ca15ea01fce1ee9a396d (round-87 C2 landing = master tip), oldest first
- date: commit date (%ad, --date=short)
- hits/files/allowed/unused_allow/scanned/rc: parsed from the scanner summary line
  `CAPTURE-SECRET-SCAN mode=rev:<sha> scanned=<n> hits=<h> files=<f> allowed=<a> unused_allow=<u> rc=<rc>`
  for `python3 -B corpus/instruments/capture-secret-scan.py --lane <lane> --rev <sha>` run in place (allowlist beside the instrument).
- lines: semicolon-joined `HIT shape=<s> path=<p> line=<n>` lines (empty when hits=0). The instrument prints no values.
- rc: 0 = clean, 1 = hits present, 2 = error (none observed; every commit ran to a summary line).
File written by ExecC2History for Kasegi round 87. No credential values appear anywhere in this dir.
