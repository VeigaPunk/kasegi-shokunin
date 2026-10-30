# R47ExecDensity — non-target guard receipts

## Scope and evidence

- Density instrument blob is unchanged: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8:corpus/instruments/density.py` and `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin hash-object /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/density.py` both printed `1f99e66f883ac2ddfd4829e83b9c037f5f0742a5`.
- Density control and tree, both invoked with `python3 corpus/instruments/density.py <SKILL.md>` from the lane repo: base export (`fc8e0af...:SKILL.md` saved in scratch) and working-tree `SKILL.md` each printed `mean dens ... 275.1`; both report 1173 lines and 34 blocks. Do-nothing control: base export. Delta is zero; if a density difference were observed it could only arise from the appended instruments-registry block, not be credited as depth. In this measurement no such difference appears.
- SHA-256, base export then tree (`sha256sum SKILL.md PROVINCE.md` equivalents): `SKILL.md b4dde6544298c11291fb0c6510036435a760dd0f4f0f8a05d3b3fc1e74b18db2`; `PROVINCE.md a9a9f62fa45cbc5f71511a645350053e13a8d66f56d06affb676ea7ab8bdbc25`. Both files match base exactly.
- Commands and printed output are retained in this seat's tool transcript; base exports and scratch were removed on shell exit. No production files, git/index, or other repositories were modified. No tool installation.

## Result / limitations

The requested non-target guard holds for `density.py`, `SKILL.md`, and `PROVINCE.md`. This establishes only blob/content identity and measured density parity for these targets; it is not evidence for other files or the round-wide claims. No do-nothing counter was run; base export is the explicit control for the comparison.
