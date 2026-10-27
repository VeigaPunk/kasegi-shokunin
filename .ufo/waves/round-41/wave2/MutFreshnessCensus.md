# MutFreshnessCensus — round 41 falsify

## Probe status

Incomplete / inconclusive: the required two mutations were not run. The attempted scratch probe extracted the pristine `corpus/SOURCES.md` from integrated ref `ad7147532cb702b0d541d40499874552183d9132`, but no modified registry bytes or mutation transcripts were produced. No mutant verdict or restored-byte hash comparison is claimed.

## Live re-open

Read the frozen `claims.json` and `scripts/sources-census.sh`. The validator contract documents E04 as “duplicate URL+scope (no supersedes)” and W04 as “same URL across scopes”; `overdue` evaluates ISO dates and `NNd` cadence, while symbolic cadences are reported, not judged overdue. Frozen C2 kill rule names a “junk twin” and many specified integrity failures, but does not expressly name an overdue mined row or a duplicate URL carrying an invalid/no-target `supersedes` marker. That is a textual observation, not an executed finding.

Executed pristine command:

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`

Output:

```
kasegi\tW04\tS028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi\tW04\tS029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi\tok\t/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

Pristine S063 row was observed at the integrated ref; it uses `opened=2026-10-27`, `recheck=on-release`, and source URL `https://www.rfc-editor.org/rfc/rfc9116.txt`. No counter-run of the requested overdue-date mutation or duplicate-URL-with-invalid-supersedes mutation was completed, so whether validate catches either remains untested here. No conclusion on detector kill/survival, no transcript, and no restoration evidence.
