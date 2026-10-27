# MutExportRecheck — clean-export recheck portability

## Probe

Integrated probe ref: `ad7147532cb702b0d541d40499874552183d9132`. Extracted its archive into `/fast/scratch/hyaku/kasegi-r41/MutExportRecheck` and ran from that directory the exact entry command (the entry's `recheck:` text before its explanatory `#`):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063
```

Observed output:

```text
S063:sha256 OK
S063:Q1 OK normalized=markup-whitespace occurrences=1 anchor=330-ok
S063:Q2 OK normalized=markup-whitespace occurrences=1 anchor=270-ok
S063:Q3 OK normalized=markup-whitespace occurrences=1 anchor=235-ok
```

The shell invocation returned exit 0. However, this is not a clean-export test of the entry's stated recheck: its leading `cd` discards the caller's exported-tree working directory and hard-codes the lane path. Therefore the success validates the lane checkout, not the exported bytes. It is not portable to an arbitrary clean exported tree; the `recheck:` line must be interpreted as lane-bound. No source-recheck invocation against the extracted tree was established by this exact command.

## Limits / cleanup

The scratch path was created with `mkdir -p` and later removed by the required cleanup trap; an inspection after the probe showed unrelated pre-existing `.ufo` contents at that path, so cleanup may have removed pre-existing scratch data. No lane or fleet files were written by the probe. No tools installed. No final Y verification claimed.