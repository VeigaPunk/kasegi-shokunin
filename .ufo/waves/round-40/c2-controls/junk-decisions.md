# Junk control — fabricated decisions (do-nothing baseline, rounds 40)

This file models the cheapest control that skips the claimed C2 work: all nine
queued rows are flipped to `rejected` with a generic reason, no source opened,
no quote, no capture, no knowledge entry, no Gate-block evidence. It must be
rejected by the frozen counter: `mined` among the nine must be >= 4 and every
decided row must carry its Gate-block evidence (URL/date/quote for mined rows,
reason+flip for rejected rows).

| S-id | fabricated status | fabricated reason | evidence |
|---|---|---|---|
| S016 | rejected | no time | none |
| S017 | rejected | no time | none |
| S019 | rejected | no time | none |
| S020 | rejected | no time | none |
| S021 | rejected | no time | none |
| S022 | rejected | superseded | none |
| S023 | rejected | no time | none |
| S024 | rejected | superseded | none |
| S025 | rejected | no time | none |
