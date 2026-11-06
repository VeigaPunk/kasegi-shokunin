# Single-transform mutants of entry-gate.py

selftest = the gate's own `--selftest`; `caught_by` = probes from the 25-probe suite that flip the mutant; `pos_broken` = positive controls the mutant wrongly fails.

| mutant | selftest | probes that catch it | positive controls broken |
|---|---|---|---|
| M01_overlong_neutered | SURVIVED | p_overlong_pin | - |
| M02_overlong_threshold_250 | SURVIVED | p_overlong_pin | - |
| M03_overlong_counts_chars | KILLED | - | f10_bare_no_prose, f1_boilerplate, p_claim_no_dash, p_claim_zero_pad, p_two_spans_on_line |
| M04_mislocated_off | KILLED | f6_moved_line, p_span_padded, p_span_case_variant_extra, p_line_zero_syn | - |
| M05_mislocated_whole_snapshot | KILLED | f6_moved_line | - |
| M06_mislocated_lowerbound_dropped | SURVIVED | p_line_zero_syn | - |
| M07_unpinned_off | SURVIVED | f16_repeat_one_pin, p_pins_outside_claims, p_pin_fragment_claims | - |
| M08_unpinned_join | KILLED | - | f10_bare_no_prose, f1_boilerplate, p_claim_no_dash, p_claim_zero_pad, p_two_spans_on_line |
| M09_unpinned_reversed | SURVIVED | p_pin_fragment_claims | - |
| M10_claim_spans_from_all | SURVIVED | p_pins_outside_claims | - |
| M11_claimless_dropped_from_ok | KILLED | p_norule, p_empty_span_claims, p_rule_no_colon, p_rule_midline, p_rejected_midline | - |
| M12_claimless_spans_only | KILLED | p_norule, p_rule_no_colon, p_rule_midline, p_rejected_midline | - |
| M13_header_always_true | SURVIVED | p_header_no_recheck, p_header_other_sid, p_header_no_verified, p_header_late, p_header_dash_missing, p_header_verified_inline, p_header_recheck_suffix | - |
| M14_header_window_80 | SURVIVED | p_header_late | - |
| M15_header_source_prefix_only | SURVIVED | p_header_other_sid, p_header_dash_missing | - |
| M16_header_dash_dropped | SURVIVED | p_header_dash_missing | - |
| M17_header_verified_anywhere | SURVIVED | p_header_verified_inline | - |
| M18_header_recheck_prefix | SURVIVED | p_header_recheck_suffix | - |
| M19_claims_le | SURVIVED | p_five_claims | - |
| M20_claims_ge | SURVIVED | p_seven_claims | - |
| M21_claim_regex_loose | SURVIVED | p_claim_unnumbered | - |
| M22_claim_regex_requires_dash | SURVIVED | - | p_claim_no_dash |
| M23_span_allows_empty | SURVIVED | p_empty_span_claims | - |
| M24_span_any_line | SURVIVED | - | p_two_spans_on_line |
| M25_sid_not_escaped | SURVIVED | - | - |
| M26_line_match_casefold | SURVIVED | p_span_case_variant_extra | - |
| M27_line_match_stripped | SURVIVED | p_span_padded | - |
| M28_rule_colon_optional | SURVIVED | p_rule_no_colon | - |
| M29_rule_anywhere | SURVIVED | p_rule_midline | - |
| M30_rejected_anywhere | SURVIVED | p_rejected_midline | - |
| M31_spans_truthiness_dropped | SURVIVED | - | - |
| M32_body_first_section_only | SURVIVED | - | - |
