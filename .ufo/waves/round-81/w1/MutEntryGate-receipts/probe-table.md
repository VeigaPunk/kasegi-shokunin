# Probe suite (negative: base must FAIL; positive: base must PASS)

| probe | bucket | expect | rc | gate verdict | counters |
|---|---|---|---|---|---|
| p_dump_unsectioned | neg | fail | 1 | fail | sid=S115 claims=0 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=6 header=ok |
| p_norule | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=6 unpinned=0 header=ok |
| p_pins_outside_claims | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=12 mislocated=0 overlong=0 claimless=0 unpinned=6 header=ok |
| p_header_no_recheck | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=bad |
| p_header_other_sid | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=bad |
| p_header_no_verified | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=bad |
| p_header_late | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=bad |
| p_header_dash_missing | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=bad |
| p_header_verified_inline | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=bad |
| p_header_recheck_suffix | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=bad |
| p_claim_unnumbered | neg | fail | 1 | fail | sid=S115 claims=0 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=6 header=ok |
| p_empty_span_claims | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=5 unpinned=0 header=ok |
| p_five_claims | neg | fail | 1 | fail | sid=S115 claims=5 want=6 spans=10 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok |
| p_seven_claims | neg | fail | 1 | fail | sid=S115 claims=7 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok |
| p_rule_no_colon | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=6 unpinned=0 header=ok |
| p_rule_midline | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=6 unpinned=0 header=ok |
| p_rejected_midline | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=6 unpinned=0 header=ok |
| p_span_casefold | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=5 overlong=0 claimless=0 unpinned=5 header=ok |
| p_overlong_pin | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=1 claimless=0 unpinned=0 header=ok |
| p_pin_fragment_claims | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=5 header=ok |
| p_span_case_variant_extra | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=11 mislocated=3 overlong=0 claimless=0 unpinned=0 header=ok |
| p_span_padded | neg | fail | 1 | fail | sid=S115 claims=6 want=6 spans=6 mislocated=5 overlong=0 claimless=0 unpinned=0 header=ok |
| p_two_spans_on_line | pos | pass | 0 | pass | sid=S115 claims=6 want=6 spans=12 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok |
| p_claim_no_dash | pos | pass | 0 | pass | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok |
| p_claim_zero_pad | pos | pass | 0 | pass | sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok |
