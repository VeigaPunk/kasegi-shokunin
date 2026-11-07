| class | patv | patr | runner-authv | deployv | agentv | workspacev | pipeline-trigger | pipeline-trigger(20) |
|---|---|---|---|---|---|---|---|---|
| baseline | H | H | H | H | H | H | H | H |
| A1_entity_nosemi | M | M | M | M | M | M | M | M |
| A1_entity_semi_control | H | H | H | H | H | H | H | H |
| A2_hex_escape | M | M | M | M | M | M | M | M |
| A3_dec_nosemi | M | M | M | M | M | M | M | M |
| A3_dec_semi_control | H | H | H | H | H | H | H | H |
| A4_double_pct | M | M | M | M | M | M | M | M |
| A4_double_amp_control | H | H | H | H | H | H | H | H |
| B_wrap_lf | M | M | M | M | M | M | M | M |
| B_wrap_crlf | M | M | M | M | M | M | M | M |
| B_wrap_cont | M | M | M | M | M | M | M | M |
| C_left_alnum | M | M | M | M | M | M | M | M |
| C_right_alnum | M | M | M | M | M | M | M | M |
| C_both_alnum | M | M | M | M | M | M | M | M |
| C_left_underscore | M | M | M | M | M | M | M | M |
| D_trailing_underscore | M | M | M | M | M | M | M | M |
| D_trailing_hyphen_control | H | H | H | H | H | H | M | M |
| E_query | H | H | H | H | H | H | H | H |
| E_query_pct_eq | H | H | H | H | H | H | H | H |
| E_query_frag | H | H | H | H | H | H | H | H |
| G_prefix_20_control | H | H | H | H | H | H | H | H |
| G_prefix_21 | H | H | H | H | H | H | H | H |
| G_prefix_30 | H | H | H | H | H | H | H | H |
| F_pct_dot_upper | M | M | M | M | M | M | · | · |
| F_pct_dot_lower | M | M | M | M | M | M | · | · |
| F_u002e_dot | M | M | M | M | M | M | · | · |
| F_html_dec_dot | M | M | M | M | M | M | · | · |
| F_html_hex_dot | M | M | M | M | M | M | · | · |

per-class: Counter({('baseline', 'HIT'): 8, ('A1_entity_nosemi', 'MISS'): 8, ('A1_entity_semi_control', 'HIT'): 8, ('A2_hex_escape', 'MISS'): 8, ('A3_dec_nosemi', 'MISS'): 8, ('A3_dec_semi_control', 'HIT'): 8, ('A4_double_pct', 'MISS'): 8, ('A4_double_amp_control', 'HIT'): 8, ('B_wrap_lf', 'MISS'): 8, ('B_wrap_crlf', 'MISS'): 8, ('B_wrap_cont', 'MISS'): 8, ('C_left_alnum', 'MISS'): 8, ('C_right_alnum', 'MISS'): 8, ('C_both_alnum', 'MISS'): 8, ('C_left_underscore', 'MISS'): 8, ('D_trailing_underscore', 'MISS'): 8, ('E_query', 'HIT'): 8, ('E_query_pct_eq', 'HIT'): 8, ('E_query_frag', 'HIT'): 8, ('G_prefix_20_control', 'HIT'): 8, ('G_prefix_21', 'HIT'): 8, ('G_prefix_30', 'HIT'): 8, ('D_trailing_hyphen_control', 'HIT'): 6, ('F_pct_dot_upper', 'MISS'): 6, ('F_pct_dot_lower', 'MISS'): 6, ('F_u002e_dot', 'MISS'): 6, ('F_html_dec_dot', 'MISS'): 6, ('F_html_hex_dot', 'MISS'): 6, ('D_trailing_hyphen_control', 'MISS'): 2})
total rows 214 hits 86 misses 128
