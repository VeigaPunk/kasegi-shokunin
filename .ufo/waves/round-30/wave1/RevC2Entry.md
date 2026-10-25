# F14 non-author bar-check

**Verdict: ADMIT. Gate: agree.** Reviewed the single F14 entry against Q1–Q10 and the round-30 captured-source assertions. No actionable admission failure found.

## Evidence

- **Measured bytes:** entry SHA-256 `f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32`; manifest `dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6`; S046 `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3`; S047 `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4`; S041 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`.
- **Q1/Q2/Q3:** Three `source:` lines directly follow title and identify S046/S047/S041 with URLs, exact captured locations; `verified-at` is dated and each load-bearing subject is supported with specific cited material. Entry states the named organizations' claims, not independent/universal facts.
- **Q4/Q5/Q6:** Attribution is explicit in text and dedicated boundary section; three checkable falsifiable checks and rejected over-generalizations are present; documentation-only and no credentials/private URLs are stated and content does not direct target activity.
- **Q7/Q10:** The recheck is one executable chained command. `bash -n` passed; foreign-cwd execution from `/tmp` passed; `cd <lane-root> &&` is included; trailing human note is after `#`.
- **Q8/Q9:** Normalization is declared by recheck output where applied (`normalized=markup-whitespace`). Ran source-recheck separately for each source: all manifest digests and assertions passed. S046 Q1–Q4 observed occurrences 1; S047 Q1/Q3 had repeated matches but verified anchors 123 and 130, respectively, and other assertions were exactly once; S041 Q1–Q3 exactly once. Manifest ids and entry source ids match exactly (S046, S047, S041); the command invokes all three with `--source`.

## Residual risk / verification gaps

This is a pinned-capture recheck, not a fresh network verification. I did not run the full frontier/census harness; this seat's review is the F14 entry/capture admission bar-check.