# Independent quarantine-slice recheck — round 30

Axes: coverage (independent row sampling) and depth:verifiability (source-grounded verdicts).

Sampled three of the seven kasegi rows in `ScoutQuarantineSlice.md`; checked local fetched evidence and corresponding register row. Verdicts concern whether the register's cited-source/quote status is supported by the available capture, not broader source authenticity.

| Row | Verdict | Evidence / reason |
|---|---|---|
| S037 (checked ABSENT) | **Disagree with ABSENT verdict.** | The register asserts the quoted metadata is absent, but `wave1/fetch/s037.html:431-446,461-474,517-527` contains GB/T 30279-2020, the Chinese title, status 现行, and publication/implementation dates exactly matching the quote. This is direct counterevidence to the absent classification. The capture sha and status are unmeasured here; no conclusion beyond this captured evidence. |
| S054 (checked ABSENT) | **Agree with the slice's ABSENT classification as a quarantine finding, with qualification.** | `wave1/fetch/s054.pdf:15` contains the exact quote 「脆弱性の悪用が確認されたもの又は疑われるもの」, so it is not absent from this local capture. The register's claim is that the earlier checked payload lacked the quote; the new local capture does not establish the prior register's fetch bytes, but it shows the quote is now verifiable and the row should not remain characterized as currently unsupported. |
| S048 (NEVER CHECKED) | **Agree.** | `wave1/fetch/s048.html` is an HTTP 404 error page identifying the requested GB detail JSP as not found; it is not the standard payload and does not verify any quote. Correctly remains unreachable/unverified rather than fabrication. |

Coverage boundary: 3/7 independently reopened; not sampled: S065, S068, S069, S070. S069/S070 are identical directory-ending locators per the slice; this review does not resolve their suspected truncation. No live bounty target contacted and no tools installed. No build/tests run (review-only assignment).
