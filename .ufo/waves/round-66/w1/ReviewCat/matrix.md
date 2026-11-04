| Probe | BASE rc/reason | Candidate rc/reason | Native stages (both runs) |
|---|---|---|---|
| `single-large` | `0/-` | `0/-` | `[-13, 0]` |
| `stdin-only-large` | `0/-` | `0/-` | `[-13, 0]` |
| `dash-only-large` | `0/-` | `0/-` | `[-13, 0]` |
| `separator-only-stdin` | `0/-` | `0/-` | `[-13, 0]` |
| `separator-single` | `0/-` | `0/-` | `[-13, 0]` |
| `separator-dash-stdin` | `0/-` | `0/-` | `[-13, 0]` |
| `single-spaced-name` | `0/-` | `0/-` | `[-13, 0]` |
| `single-escaped-name` | `0/-` | `0/-` | `[-13, 0]` |
| `single-operator-name` | `0/-` | `0/-` | `[-13, 0]` |
| `literal-option-name` | `0/-` | `0/-` | `[-13, 0]` |
| `literal-separator-name` | `0/-` | `0/-` | `[-13, 0]` |
| `later-missing-large` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `earlier-missing-large` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `two-existing-large` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `same-file-twice` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `separator-two-existing` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `separator-later-missing` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `separator-earlier-missing` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `dash-before-file` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `file-before-dash` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `two-dashes` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `stdin-before-missing` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `missing-before-stdin` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `option-u-single` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `option-n-single` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `long-option-single` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `option-and-separator` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `option-multi` | `0/-` | `1/derive-upstream-signal-13` | `[-13, 0]` |
| `single-small` | `0/-` | `0/-` | `[0, 0]` |
| `two-existing-small` | `0/-` | `0/-` | `[0, 0]` |
| `later-missing-small` | `1/derive-upstream-exit-1` | `1/derive-upstream-exit-1` | `[1, 0]` |
| `earlier-missing-small` | `1/derive-upstream-exit-1` | `1/derive-upstream-exit-1` | `[1, 0]` |
| `missing-only` | `1/derive-upstream-exit-1` | `1/derive-upstream-exit-1` | `[1, 0]` |
| `multi-drained` | `0/-` | `0/-` | `[0, 0]` |
| `multi-drained-later-missing` | `1/derive-upstream-exit-1` | `1/derive-upstream-exit-1` | `[1, 0]` |
| `grep-nomatch` | `0/-` | `0/-` | `[1, 0]` |
| `other-head-sigpipe` | `0/-` | `0/-` | `[-13, 0]` |
| `other-cut-sigpipe` | `0/-` | `0/-` | `[-13, 0]` |
| `upstream-positive-seven` | `1/derive-upstream-exit-7` | `1/derive-upstream-exit-7` | `[7, 0]` |
| `upstream-signal-fifteen` | `1/derive-upstream-signal-15` | `1/derive-upstream-signal-15` | `[-15, 0]` |
| `final-error-precedence` | `1/derive-exit-2` | `1/derive-exit-2` | `[-13, 2]` |
| `middle-multi-cat` | `0/-` | `1/derive-upstream-signal-13` | `[-13, -13, 0]` |
| `middle-single-cat` | `0/-` | `0/-` | `[-13, -13, 0]` |
