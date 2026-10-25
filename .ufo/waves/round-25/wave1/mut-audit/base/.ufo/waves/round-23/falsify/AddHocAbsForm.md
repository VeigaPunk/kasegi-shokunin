# R23 falsify — absolute-form bounty prefix (`/home/vgpnk/Projects/bounties-legacy/...`)

Seat: `L1Kasegi23.AddHocAbsForm-2` (leaf, no dispatch).
Target as assigned: build a scratch harness that runs the copied CLI over a temp HOME whose
`Projects/` tree contains only `bounties-legacy/README.md`, with a mirror containing
`-legacy/README.md`, citing the **absolute** form
`/home/vgpnk/Projects/bounties-legacy/README.md:1`; report the class for fixed and baseline
bytes and say whether the absolute prefix is covered by `bounty_suffix()`'s boundary or only by
the tilde form.

No production file, lane tree, git/jj state, or sibling lane was written. Only this report was
written, plus scratch under `/tmp/kasegi-r23-falsify-AddHocAbsForm/`. No commits, no installs,
no package transactions. Read-only claims below are all reproduced from bytes, not repeated from
the L1.

## Answer (both halves)

1. **The absolute spelling is covered by `bounty_suffix()`'s boundary, through the second
   frozen `BOUNTY_PREFIXES` entry — not through the tilde form.** `corpus/instruments/resolve.py:97`
   hardcodes both spellings: `BOUNTY_PREFIXES = ("~/Projects/bounties", "/home/vgpnk/Projects/bounties")`.
   `bounty_suffix()` (`resolve.py:201-212`) loops both prefixes and applies the `/`-delimited
   boundary at `resolve.py:210` (`if base.startswith(root + "/")`). Under a foreign HOME the
   tilde entry cannot cover the absolute spelling at all: with
   `HOME=/tmp/kasegi-r23-falsify-AddHocAbsForm/fixed-tilde/home`,
   `expanduser("~/Projects/bounties")` →
   `/tmp/kasegi-r23-falsify-AddHocAbsForm/fixed-tilde/home/Projects/bounties`, which is not a
   prefix of `/home/vgpnk/...` (verbatim probe output below). So coverage is real, but it is
   carried by the frozen host-absolute literal, not by HOME expansion.

2. **Classes at the assigned cite (literal absent on this host):**

| bytes | SHA-256 | class | domain | mirror consulted? |
|---|---|---|---|---|
| fixed `corpus/instruments/resolve.py` | `ed9a9dae…40e9` | **GONE** | `other` | no — boundary rejects the sibling, so no bounty fallback runs |
| baseline `.ufo/waves/round-23/c1-baseline-resolver.py` | `d6a3c3f1…f903` | **MIRROR-EQUIVALENT** | `bounty` | yes — `mirror/-legacy/README.md`, a decoy credited as evidence |

Verbatim TSV rows (fixed first, baseline second):

```
/home/vgpnk/Projects/bounties-legacy/README.md:1	GONE		1		other	1	SKILL
/home/vgpnk/Projects/bounties-legacy/README.md:1	MIRROR-EQUIVALENT	/tmp/kasegi-r23-falsify-AddHocAbsForm/baseline-abs/relocated/tbh/-legacy/README.md	1	literal	bounty	1	SKILL
```

Baseline's path to the decoy is `c1-baseline-resolver.py:204` (`base.startswith(BOUNTY_PREFIXES)`,
a bare prefix tuple) then `:206` (`base.split("/Projects/bounties", 1)[1].lstrip("/")` →
`-legacy/README.md`) then `:210-212` (mirror join → `MIRROR-EQUIVALENT`, no `under_mirror` call
in that branch). Fixed replaces it with `resolve.py:225-234`: `bounty_suffix()` returns `None` for
the sibling, so the token falls through to the ordinary-other-root branch and `GONE`.

## Harness and bytes (reproducible)

Scratch (`/tmp/kasegi-r23-falsify-AddHocAbsForm/`):

> Durability note (2026-10-25T03:46-03:00): this report cites **no** `.ufo/…/scratch` path, so the
> fleet-wide round-35 relocation (`.ufo/waves/round-35/scratch/` → `scratch-evidence/`) cannot
> dangle it; this repo has only `.ufo/waves/round-23`. Its scratch is a `/tmp` tree, verified intact
> at that timestamp with the two script hashes below unchanged. Every output quoted in this report
> is inlined rather than left in scratch (verbatim TSV rows, CLI stdout, probe table, mutant diffs,
> matrix receipts), so the evidence stands even if `/tmp` is cleared; the scratch paths are
> provenance, not a data dependency. No file here is rebuilt from transcript — every SHA-256 in this
> report is of the bytes that were measured.

- `harness.py` (`87f7801684adcc03ce19ff5b8855d6dc3ad5f633cde239a16c12b05537ff8916`) — copies the
  resolver bytes next to a disposable tree, so the CLI's own `citation-survival.tsv` is written in
  scratch, never in the repo.
- `prefix-probe.py` (`b1c996c12fc335d347f6bb3b3a448fce113c1044f38953da81daddacc8fdeffe`) —
  in-process `bounty_suffix()` / `classify()` / `under_mirror()` table.
- `bytes-fixed.py` = `ed9a9dae…40e9`, `bytes-baseline.py` = `d6a3c3f1…f903` (staged before the
  namespace arm, because the bind mount hides the repo path).
- `mutant-boundary-removed.py` (`1d72491a77f662bccf2cc1eb48c7c6c8f60808d9e0d9204baee4bda8ba5dc73c`)
  — scratch-only, `root + "/"` → `root`, suffix slice takes `base[len(root):]`:
  this reproduces the baseline's `-legacy` mapping while keeping `under_mirror`.
- `mutant-abs-prefix-dropped.py` (`f032c4ca91530cf6c644a0ff08bcaa197959d660591fc05de66d58df9c4db71f`)
  — scratch-only, `BOUNTY_PREFIXES` loses its absolute entry.

Layout per arm: `home/Projects/bounties-legacy/README.md` (only entry under `Projects/`),
`relocated/tbh/-legacy/README.md` (mirror decoy), `lane/SKILL.md` = `` - `<cite>` ``,
`tool/resolve.py` = bytes under test; env `HOME`, `KASEGI_MIRROR`, `PATH`, `LANG=C.UTF-8`,
`PYTHONDONTWRITEBYTECODE=1`.

Exact invocation for the assigned arm:

```
python3 /tmp/kasegi-r23-falsify-AddHocAbsForm/harness.py \
  --resolver /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py \
  --root /tmp/kasegi-r23-falsify-AddHocAbsForm/fixed-abs --label fixed-abs
```

CLI output for fixed: `distinct=1 resolves=0 mirror=0 internal=0 other=0 gone=1 skill=0/1 corpus=0/0 all=0/1`.

### Cross-check arms

| arm | cite | fixed | baseline | boundary-removed mutant |
|---|---|---|---|---|
| absent literal (assigned) | `/home/vgpnk/Projects/bounties-legacy/README.md:1` | GONE / other | MIRROR-EQUIVALENT / bounty | MIRROR-EQUIVALENT / bounty |
| literal present (private ns bind) | same | RESOLVES literal / other | RESOLVES literal / bounty | RESOLVES literal / bounty |
| tilde spelling | `~/Projects/bounties-legacy/README.md:1` | RESOLVES literal / other | RESOLVES literal / bounty | RESOLVES literal / bounty |
| absolute ancestor traversal, decoy at `relocated/outside.md` | `/home/vgpnk/Projects/bounties/../outside.md:1` | GONE / bounty | MIRROR-EQUIVALENT → `relocated/tbh/../outside.md` | GONE / bounty |
| absolute double-slash | `/home/vgpnk/Projects/bounties//etc/hostname:1` | GONE / bounty | — | — |
| legit absolute bounty cite, decoy at mirror `ops/rank.mjs` | `/home/vgpnk/Projects/bounties/ops/rank.mjs:1` | MIRROR-EQUIVALENT / bounty | MIRROR-EQUIVALENT / bounty | MIRROR-EQUIVALENT / bounty (absolute-prefix-dropped: **GONE / other**) |

The `literal present` arm needs a real `/home/vgpnk/Projects/bounties-legacy/README.md`, which the
contract forbids creating, so it ran in a private mount namespace:

```
unshare -rm --propagation private sh -c \
  "mount --bind /tmp/kasegi-r23-falsify-AddHocAbsForm/present-projects /home/vgpnk/Projects && \
   python3 /tmp/kasegi-r23-falsify-AddHocAbsForm/harness.py --resolver /tmp/kasegi-r23-falsify-AddHocAbsForm/bytes-fixed.py \
     --root /tmp/kasegi-r23-falsify-AddHocAbsForm/fixed-abs-present --label fixed-abs-present"
```

Inside: `abs path exists : /home/vgpnk/Projects/bounties-legacy/README.md -> True`,
row `…/bounties-legacy/README.md:1	RESOLVES	/home/vgpnk/Projects/bounties-legacy/README.md	1	literal	other	1	SKILL`.
After exit the host is unchanged: `ls -d /home/vgpnk/Projects/bounties*` → absent,
`findmnt -no TARGET /home/vgpnk/Projects` → not a host mount point. The boundary therefore does not
over-block a legitimately present absolute sibling file; it only re-tags it as the ordinary other
root it is.

In-process table (`prefix-probe.py`, fixed bytes, foreign HOME):

```
BOUNTY_PREFIXES = ('~/Projects/bounties', '/home/vgpnk/Projects/bounties')
  prefix '~/Projects/bounties'  expanduser -> '/tmp/kasegi-r23-falsify-AddHocAbsForm/fixed-tilde/home/Projects/bounties'
  prefix '/home/vgpnk/Projects/bounties'  expanduser -> '/home/vgpnk/Projects/bounties'
bounty_suffix('/home/vgpnk/Projects/bounties-legacy/README.md'  ) -> None
bounty_suffix('/home/vgpnk/Projects/bounties-x/README.md'       ) -> None
bounty_suffix('/home/vgpnk/Projects/bounties/ops/rank.mjs'      ) -> 'ops/rank.mjs'
bounty_suffix('/home/vgpnk/Projects/bounties'                   ) -> ''
bounty_suffix('/home/vgpnk/Projects/bounties/'                  ) -> ''
bounty_suffix('/home/vgpnk/Projects/bounties//etc/hostname'     ) -> '/etc/hostname'
bounty_suffix('/home/vgpnk/Projects/bounties/../outside.md'     ) -> '../outside.md'
bounty_suffix('~/Projects/bounties-legacy/README.md'            ) -> None
classify('/home/vgpnk/Projects/bounties-legacy/README.md') -> ('GONE', '', '', 'other')
join(mirror, '/etc/hostname') -> '/etc/hostname'
under_mirror(/etc/hostname, mirror) -> False
under_mirror(mirror + /../outside.md, mirror) -> False
```

## Findings

**F1 — Confirmed, falsifiable: the frozen C1 matrix does not pin the absolute arm in either
direction; a regression that drops `BOUNTY_PREFIXES[1]` passes all 13 cases.**

Replay with the matrix's own driver:

```
python3 corpus/instruments/mirror-containment-check.py \
  --resolver /tmp/kasegi-r23-falsify-AddHocAbsForm/mutant-abs-prefix-dropped.py \
  --json /tmp/kasegi-r23-falsify-AddHocAbsForm/mutant2-matrix.json
→ cases=13 escape=6 controls=7 pass=13 fail=0
  resolver_sha256=f032c4ca91530cf6c644a0ff08bcaa197959d660591fc05de66d58df9c4db71f
  matrix_sha256=5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9
```

Yet that mutant changes observable behavior on the absolute arm:
`/home/vgpnk/Projects/bounties/ops/rank.mjs:1` goes `MIRROR-EQUIVALENT` (`bounty`, mirror
`ops/rank.mjs`) → `GONE` (`other`) — a false GONE, i.e. lost coverage, not a leak. The mutation is
invisible to the matrix because every frozen cite is tilde-spelled or relative — measured from
`mirror-containment-fixtures.json`: 7× `~/Projects/bounties…`, 2× `~/Projects/the-bounty-hunter…`,
4× relative, **0** cites beginning with `/`. Falsifiable prediction: add one absolute-form fixture
(`/home/vgpnk/Projects/bounties-legacy/README.md:1` → GONE with the `-legacy/README.md` decoy, or
`/home/vgpnk/Projects/bounties/ops/rank.mjs:1` → MIRROR-EQUIVALENT with a mirror `ops/rank.mjs`) and
the dropped-prefix mutant must fail; if it does not fail, this finding is wrong.

**F2 — The boundary itself *is* pinned, but only through the tilde spelling; the two guards are
separable and both are load-bearing.** Boundary-removed mutant against the frozen matrix:
`cases=13 escape=6 controls=7 pass=12 fail=1`, uniquely
`FAIL bounty-prefix-sibling-confusion expect GONE actual MIRROR-EQUIVALENT |
~/Projects/bounties-legacy/README.md:1`. That same mutant still returns **GONE** for the absolute
ancestor-traversal cite (decoy at `relocated/outside.md`) while the baseline returns
`MIRROR-EQUIVALENT` to `relocated/tbh/../outside.md`: `under_mirror()` (`resolve.py:215-220`, called
at `:232`) independently stops traversal, and the prefix boundary independently stops the `-legacy`
sibling. Neither guard alone covers both escapes, so a future "simplify one helper" edit breaks one
family while the other stays green. The double-slash probe (`bounty_suffix` → `/etc/hostname`,
`os.path.join` discards the mirror prefix, `under_mirror` → `False`) returns GONE — no leak there,
and it shows `under_mirror` is what makes the leaking join harmless.

**F3 — Coverage/portability note (not a defect in the landed bytes).** Absolute-arm containment is
hardcoded to this host's spelling (`resolve.py:97`). Nothing in `bounty_suffix()`'s docstring
(`:201-204`) says the absolute alias is host-frozen; the docstring only promises "the exact bounty
root". On any tree checked out under a different home the absolute spelling necessarily degrades to
an ordinary other root — behaviorally identical to the dropped-prefix mutant. That is a design
consequence of `BOUNTY_PREFIXES`, so the fix is host-specific while the boundary is not.

## Scope limits

- The host has no bounty tree: `ABSENT /home/vgpnk/Projects/bounties`,
  `ABSENT /home/vgpnk/Projects/bounties-legacy`, and both `MIRROR_CANDIDATES` are absent, so the
  assigned cite's *literal* branch can never fire here. The absent arm is real; the present arm is
  synthetic (private namespace bind), and it can only show class/domain, not the production snapshot.
- Production impact today is nil: the lane's absolute bounty tokens are 14× `/home/vgpnk/Projects/bounties`
  and 1× `/home/vgpnk/Projects/bounties/claims` (all `GONE`, domain `bounty`, under fixed bytes
  too), so fixed and the dropped-prefix mutant classify them identically. F1 is a pin gap, not a
  live misclassification.
- Judged only the detector's classification. This establishes nothing about source availability,
  corpus attribution, admission, or any score movement; no admission is claimed.
- Editing wave: no build, lint, test, type-check, or formatter run was performed (parent owns the
  post-integration gate). All mutants and outputs live in `/tmp`; repo bytes were read only.

## Appendix — verbatim scratch sources

Both scripts are inlined byte-for-byte, so the report is self-contained: if `/tmp` is cleared,
extract each block and the SHA-256 quoted above must match the extracted file. Nothing here is
rebuilt from transcript — these are the bytes that produced the quoted arm output.

### `harness.py` — `87f7801684adcc03ce19ff5b8855d6dc3ad5f633cde239a16c12b05537ff8916`

```python
#!/usr/bin/env python3
"""Scratch r23 falsify probe: absolute-form prefix-sibling of the bounty root.

Builds a disposable tree with an isolated HOME whose Projects tree contains
only `bounties-legacy/README.md`, a KASEGI_MIRROR containing `-legacy/README.md`
(the old '-' suffix decoy), and a lane SKILL.md citing one token. Copies the
resolver bytes under test next to the tree (so its written TSV stays in
scratch) and runs the untouched CLI once.

Prints the CLI exit/stdio and every TSV row verbatim, plus byte identity and
the on-disk state of the absolute path the citation names.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

ABS_CITE = "/home/vgpnk/Projects/bounties-legacy/README.md"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def build(root, cite):
    home = os.path.join(root, "home")
    mirror = os.path.join(root, "relocated", "tbh")
    lane = os.path.join(root, "lane")
    tool = os.path.join(root, "tool")
    for d in (os.path.join(home, "Projects", "bounties-legacy"),
              os.path.join(mirror, "-legacy"),
              lane, tool):
        os.makedirs(d, exist_ok=True)
    with open(os.path.join(home, "Projects", "bounties-legacy", "README.md"),
              "w", encoding="utf-8") as fh:
        fh.write("ordinary other-root literal under the disposable HOME\n")
    with open(os.path.join(mirror, "-legacy", "README.md"), "w",
              encoding="utf-8") as fh:
        fh.write("decoy under the selected mirror reached by a '-' suffix\n")
    with open(os.path.join(lane, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("# abs-form probe\n\n- `%s`\n" % cite)
    return home, mirror, lane, tool


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--resolver", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--cite", default=ABS_CITE + ":1")
    ap.add_argument("--label", default="")
    ap.add_argument("--extra-file", action="append", default=[],
                    help="path relative to --root to materialise before the run")
    args = ap.parse_args(argv)

    shutil.rmtree(args.root, ignore_errors=True)
    home, mirror, lane, tool = build(args.root, args.cite)
    for rel in args.extra_file:
        target = os.path.join(args.root, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write("decoy planted at %s\n" % rel)
    copied = os.path.join(tool, "resolve.py")
    shutil.copyfile(args.resolver, copied)

    env = {
        "HOME": home,
        "KASEGI_MIRROR": mirror,
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    proc = subprocess.run([sys.executable, copied, lane], cwd=tool, env=env,
                          capture_output=True, text=True, timeout=120)

    print("label            : %s" % args.label)
    print("resolver         : %s" % args.resolver)
    print("resolver sha256  : %s" % sha256_file(args.resolver))
    print("copied sha256    : %s" % sha256_file(copied))
    print("cite             : %s" % args.cite)
    print("HOME             : %s" % home)
    print("KASEGI_MIRROR    : %s (realpath %s)" % (mirror, os.path.realpath(mirror)))
    print("abs path exists  : %s -> %s"
          % (ABS_CITE, os.path.exists(ABS_CITE)))
    print("decoy exists     : %s"
          % os.path.exists(os.path.join(mirror, "-legacy", "README.md")))
    print("cli exit         : %d" % proc.returncode)
    print("cli stdout       : %s" % (proc.stdout or "").strip())
    if proc.stderr.strip():
        print("cli stderr       : %s" % proc.stderr.strip()[:400])

    tsv = os.path.join(tool, "citation-survival.tsv")
    print("tsv              : %s (exists %s)" % (tsv, os.path.isfile(tsv)))
    if os.path.isfile(tsv):
        with open(tsv, "r", encoding="utf-8") as fh:
            for line in fh:
                print("row              : %s" % line.rstrip("\n"))
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

### `prefix-probe.py` — `b1c996c12fc335d347f6bb3b3a448fce113c1044f38953da81daddacc8fdeffe`

```python
#!/usr/bin/env python3
"""In-process probe: which BOUNTY_PREFIXES entry grants bounty_suffix() the
absolute spelling, and what the tilde entry expands to under a foreign HOME.

Run as:
  env HOME=/tmp/kasegi-r23-falsify-AddHocAbsForm/fixed-tilde/home \
      KASEGI_MIRROR=/tmp/kasegi-r23-falsify-AddHocAbsForm/fixed-tilde/relocated/tbh \
      python3 /tmp/kasegi-r23-falsify-AddHocAbsForm/prefix-probe.py \
      /tmp/kasegi-r23-falsify-AddHocAbsForm/bytes-fixed.py
"""
import importlib.util
import os
import sys

spec = importlib.util.spec_from_file_location("res", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

print("module      :", m.__file__)
print("HOME        :", os.environ["HOME"])
print("KASEGI_MIRROR:", os.environ["KASEGI_MIRROR"])
print("BOUNTY_PREFIXES =", m.BOUNTY_PREFIXES)
for p in m.BOUNTY_PREFIXES:
    print("  prefix %r\n    expanduser -> %r" % (p, os.path.expanduser(p)))

toks = [
    "/home/vgpnk/Projects/bounties-legacy/README.md",
    "/home/vgpnk/Projects/bounties-x/README.md",
    "/home/vgpnk/Projects/bounties/ops/rank.mjs",
    "/home/vgpnk/Projects/bounties",
    "/home/vgpnk/Projects/bounties/",
    "/home/vgpnk/Projects/bounties//etc/hostname",
    "/home/vgpnk/Projects/bounties/../outside.md",
    "~/Projects/bounties-legacy/README.md",
    "~/Projects/bounties/ops/rank.mjs",
]
for t in toks:
    print("bounty_suffix(%-56r) -> %r" % (t, m.bounty_suffix(t)))

lane = os.path.join(os.environ["HOME"], "..", "lane")
mirror = os.environ["KASEGI_MIRROR"]
for t in (toks[0], toks[5], toks[6], toks[7]):
    print("classify(%-56r) -> %r" % (t, m.classify(t, lane, mirror)))

print("join(mirror, %r) -> %r"
      % ("/etc/hostname", os.path.join(mirror, "/etc/hostname")))
print("under_mirror(/etc/hostname, mirror) ->",
      m.under_mirror("/etc/hostname", mirror))
print("under_mirror(mirror + /../outside.md, mirror) ->",
      m.under_mirror(os.path.join(mirror, "../outside.md"), mirror))
print("MIRROR_ROOT/MIRROR_ABSENT ->", m.MIRROR_ROOT, m.MIRROR_ABSENT)
```
