# LabScratchClean — round-40 falsify wave 2 receipt

Attacked item: scratch hygiene (H6 live check) — stray `kasegi-r39*` / `kasegi-r40*` dirs under `/fast/scratch/hyaku/`.
Commands re-run: `ls -la --time-style=full-iso /fast/scratch/hyaku/ | grep -E 'kasegi-r39|kasegi-r40'`; `ls -la /fast/scratch/hyaku/kasegi-r40/` (x2); `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`; `ls -d` of kasegi* under /tmp, /var/tmp, /fast/scratch, /fast/scratch/hyaku/*/; wave2-spec.json seat-name extraction.
Fetch/time: listing at 2026-10-26T22:06:35Z (19:06:35 -0300); re-list 22:06:54Z.

## Listing (result: reproduced clean — no defect)
- `kasegi-r39*` under /fast/scratch/hyaku: NONE.
- `kasegi-r40*` under /fast/scratch/hyaku: only `kasegi-r40/` (the shared round work dir; created 19:06:00, 76K at listing). No `kasegi-r40-*` siblings, nothing else matching.
- Contents of `kasegi-r40/` at first listing (excluding LabScratchClean): CritCounterSoup, CritKillRule (holds r40-closure.sh, 71895 B), CritRecordsConsistency, CritSourceTruth, RevC1Counters, RevC1Sandbox, RevC2Entries, RevF23, RevH3Criterion, ScoutReopenLeads, SentinelFinal. Re-list 20 s later added ConnPatterns, CritCrossAxis, ScoutHrefCheck (RevH3Criterion now holds a subdir). All are empty or tiny, all created 19:06:06–19:06:52, i.e. seats starting up.
- Every dir name is a wave-2 seat in `wave2-spec.json` (35 seats). No dir is outside the seat roster, none predates the wave (oldest 19:06:06 vs parent created 19:06:00), none is a r39 leftover. Verdict: no stray; all are live seats' scratch.
- Siblings from other lanes (not kasegi): kaidoku-r39/r40/r41/r42, kengaku-r43, mado-r47, tabi-r35, tameshi-r50, tsukuroi-r43, kaidoku-r38 etc. — out of scope for kasegi H6; no kasegi-r39 anywhere.

## Outside the scratch root (observation, not a defect)
- `/tmp/kasegi-r40-draft/` (6 files, 14523 B: draft.md, log-line.md, report.md, scorecard-block.md, shonen-line.md, verify-at-y.sh; mtimes 18:58–19:01). This is the L1's expected work dir (report/log/scorecard drafts, verify-at-y.sh). Under the 50 MB /tmp limit. It is not under /fast/scratch/hyaku, so the `kasegi-r40*` H6 scan there does not see it. It must be removed by the L1 at close if H6 or any /tmp census covers it. No other kasegi* under /tmp (only that one), /var/tmp, /fast/scratch.

## disk-guard status (result: green)
/tmp 3% used, 125.2G free; /var/tmp 35%, 585.1G free; /fast/scratch/hyaku 24%, 617.4G free. Top consumers under /fast/scratch/hyaku are other lanes (mado-r47 3.7G, kaidoku-r41 2.1G, kaidoku-r42 1.5G, kengaku-r43 1.0G); `kasegi-r40` 76K. No /tmp item is kasegi's except the draft dir above (14.5 KB).

## Caveat for the closer
The listing is a snapshot during active wave 2: every seat dir above must be gone after all seats yield. The H6 check is only meaningful after the wave settles — re-run `ls /fast/scratch/hyaku/ | grep kasegi-r4` then; expected result is `kasegi-r40/` itself removed or empty, and `/tmp/kasegi-r40-draft` removed.
This seat's own scratch `/fast/scratch/hyaku/kasegi-r40/LabScratchClean` is removed before yield.
