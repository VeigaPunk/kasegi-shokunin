# Fixture registry — indented-row trap

Synthetic fixture. It exists only to prove the §10 id-collision guard can fail.
The second row is INDENTED by two spaces, which is legal inside a Markdown blockquote
or a nested list and is exactly what a copy-paste out of a review comment produces.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | Fixture Document Alpha — https://example.invalid/alpha | docs | A | fixture | fixture | fixture | mined | 2026-10-25 | 180d | — |
  | S002 | Fixture Document Beta — https://example.invalid/beta | docs | A | fixture | fixture | fixture | mined | 2026-10-25 | 180d | — |
