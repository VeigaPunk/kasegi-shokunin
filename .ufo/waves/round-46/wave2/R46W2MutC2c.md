VERDICT: BROKEN

# R46W2MutC2c — C2 mutation test of `corpus/instruments/r46-c2-gate.py` v1.1, gates G6–G7

Scope: gates G6 (exact knowledge directory, byte pin with the two exempt entries) and G7 (census path). Eight single-edit mutants of the committed tip, one per defect family, plus two controls. Three of the eight are NOT rejected by the counter. Two of the three (F1 directory symlink, F2 SOURCES.md symlink) pass only because of bytes outside the tree, each confirmed by moving the external target away. The third (F3, exempt entry content) is unpinned by design and is caught by C1, not C2.

## Setup (what was run, what was attacked)

- Lane HEAD is `0d121a2` (the wave-2 spec commit, a descendant of the tip). `git diff --stat 5437afe -- corpus .ufo/waves/round-46/claims.json` printed nothing and `git status --short -- corpus` printed nothing, so the worktree corpus is byte-identical to the tip `5437afe`. The tip export was made with `git -C .../kasegi-shokunin archive 5437afeaf9b642c267bba3c31f00ae701e49da68 | tar -x -C <scratch>/tree` (9214 files, 65 depth-1 `.md`).
- Counter under test: the lane's own `corpus/instruments/r46-c2-gate.py`, sha256 `b52fea3183a393fa2f5bb40879241034e9db0b45f7914244d9f3bed134958621` (= the errata's v1.1 sha; v1 is `0ee958…f2f` per `git show 9f23aab…:corpus/instruments/r46-c2-gate.py`). Not edited.
- Commands: `python3 corpus/instruments/r46-c2-gate.py --root <tree>` with `TMPDIR` set explicitly to the scratch dir; census called by the counter at its absolute constant `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (sha256 `3fb7261569f4…64e30`, read-only use).
- Recipe: `R46W2MutC2c/recipe.py` (scratch, embedded at the end of this report). Each mutant is a fresh `copytree` of the tip, one edit, then the lane counter. The recipe asserts that each defect is present before the counter runs.

Command run: `cd <scratch> && python3 recipe.py` (exit 0, 54 s). Its printed output, verbatim:

```
control=tip-copy-no-edit rejected=0 fixed=7/7 failing=-
control=do-nothing-base rejected=1 fixed=1/7 failing=G1,G2,G3,G4,G5,G6
mutant=knowledge-dir-symlink rejected=0 defect_present=1 fixed=7/7 failing=- edit=[corpus/knowledge replaced by a symlink to /fast/scratch/hyaku/kasegi-r46/R46W2MutC2c/ext/knowledge-copy (identical 65 bytes, outside the tree); find(-P) lists 0 files]
mutant=exempt-entry-gutted rejected=0 defect_present=1 fixed=7/7 failing=- edit=[replace the whole body of exempt claim-gates.md with one heading line]
mutant=sources-md-symlink-external rejected=0 defect_present=1 fixed=7/7 failing=- edit=[corpus/SOURCES.md replaced by a symlink to /fast/scratch/hyaku/kasegi-r46/R46W2MutC2c/ext/sources-root/corpus (identical bytes; census realpath resolves used-by against the external root)]
mutant=knowledge-nested-md rejected=1 defect_present=1 fixed=6/7 failing=G6 edit=[new file corpus/knowledge/archive/old-entry.md (nested .md, depth 2)]
mutant=base-entry-one-byte-drift rejected=1 defect_present=1 fixed=6/7 failing=G6 edit=[append one newline byte to linux-kernel-security-bugs-reporting-process.md (base entry, not exempt)]
mutant=exempt-entry-renamed rejected=1 defect_present=1 fixed=6/7 failing=G6 edit=[rename claim-gates.md -> claim-gate.md (bytes unchanged; exempt name is pinned)]
mutant=census-duplicate-row rejected=1 defect_present=1 fixed=6/7 failing=G7 edit=[append a verbatim copy of the S001 registry row directly after it (duplicate id)]
mutant=census-dangling-usedby rejected=1 defect_present=1 fixed=6/7 failing=G7 edit=[S001 row (mined) used-by cell -> corpus/knowledge/cvss-v4-dangling.md (path not on disk)]
cross-check=C1 mutant=exempt-entry-gutted rejected=1 line=[c1-gate fixed=0/7 exit=1]
```

Control on the tip itself (the lane's counter, unmodified tree): `gate G1..G7 pass=1 … c2-gate fixed=7/7 exit=0` (verbatim per-gate reads: `G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1`, `G7 pass=1 read=census-rc=0 ok-line=1`).

## Survivors (the findings)

### F1 — SURVIVES: `knowledge-dir-symlink` (G6 "exact knowledge directory")

- Edit (one tree entry): `corpus/knowledge/` replaced by a symlink to an identical copy of the 65 files **outside** the tree (`$S/ext/knowledge-copy`).
- Counter, verbatim: `gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1` and `c2-gate fixed=7/7 exit=0`.
- Defect is present: `ls -l …/corpus | grep knowledge` → `lrwxrwxrwx … knowledge -> /fast/scratch/hyaku/kasegi-r46/R46W2MutC2c/ext/knowledge-copy`. The docstring's own G6 command, `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l`, yields `0` on this tree (recipe's `find(-P) lists 0 files`), so the sentence the code is supposed to implement (`== 65`) is false for this tree while the code says pass.
- Cause: `corpus/instruments/r46-c2-gate.py:306-310` uses `os.path.isdir` / `os.listdir` / `os.walk`, which follow a symlinked directory; no `islink` test exists for the directory (only for the F28 entry, line 160).
- Passing is entirely external: moving the external copy away (`mv ext/knowledge-copy ext/knowledge-copy.away`) gives `gate G6 pass=0 read=knowledge=0 entries=0 nested-md=0 base-intact=0 entry-bytes-ok=0`, `gate G5 pass=0 read=F28-entry-not-a-regular-file`, `c2-gate fixed=1/7 exit=1`.

### F2 — SURVIVES: `sources-md-symlink-external` (G7 "census path")

- Edit: `corpus/SOURCES.md` replaced by a symlink to an identical copy of `corpus/` **outside** the tree (`$S/ext/sources-root/corpus`).
- Counter, verbatim: `gate G7 pass=1 read=census-rc=0 ok-line=1`, `c2-gate fixed=7/7 exit=0`.
- Mechanism: the census in `--file` mode resolves `file_abs=$(realpath -- "$FILE")` and sets `dir_abs` to the realpath's root (`sources-census.sh:500-502`), and E11 checks used-by paths against that root (`:567`). The counter passes the un-resolved tree path (`counter:324`), so the census validates the external registry and its external used-by targets, not the tree's.
- Passing is entirely external: with `mv ext/sources-root ext/sources-root.away`, the same tree reads `gate G7 pass=0 read=census-rc=2 ok-line=0` and `c2-gate fixed=5/7 exit=1`.

### F3 — SURVIVES by design, but C2 is blind to it: `exempt-entry-gutted` (G6 "byte pin with the two exempt entries")

- Edit: the whole body of `corpus/knowledge/claim-gates.md` (exempt) replaced by `# claim gates`. The restoration-recheck line and the C1 Re-ground section are both gone.
- Counter: `c2-gate fixed=7/7 exit=0`, because `CONTENT_EXEMPT = {"claim-package-contract.md", "claim-gates.md"}` (`counter:68`) removes the two entries from the content pin, and the names pin still holds.
- Surgical variant (drop only `## Re-ground (round 46)` through EOF, keep base lines and the recheck): C2 still `fixed=7/7 exit=0`. C1 reads `gate L1 pass=0 read=gated=23 … L2 pass=0 read=base-gated=24 regrounded=1 claim-package-contract.md … L7 pass=0 read=still-gated=23 changed=claim-gates.md … c1-gate fixed=4/7 exit=1`. So the exempt-content hole is closed by C1 (L1, L2, L7) and not by C2.
- Caveat on the first C1 run: on the full gutting, C1 printed `gate L1..L7 pass=0 read=exception-KeyError` / `c1-gate fixed=0/7 exit=1` — a crash on every limb, not a targeted reject. The C1 tip control reads `c1-gate fixed=7/7 exit=0` (`L6 … mutants=46 survivors=none`), so the C1 cross-check is discriminating but its gutted-entry reject is by exception. Flagged for the C1 owner.

## Rejected, as expected (discrimination)

- `knowledge-nested-md` → `G6 pass=0`, fixed 6/7 (nested `.md` at depth 2 raises the os.walk count to 66; `counter:310`).
- `base-entry-one-byte-drift` → `G6 pass=0 read=… base-intact=0`, fixed 6/7 (one newline byte in a non-exempt base entry; base content pin, `counter:315-318`).
- `exempt-entry-renamed` → `G6 pass=0`, fixed 6/7 (exempt name pinned; `claim-gates.md` → `claim-gate.md`, bytes unchanged).
- `census-duplicate-row` → `G7 pass=0`, fixed 6/7 (census E03 on a copied S001 row).
- `census-dangling-usedby` → `G7 pass=0`, fixed 6/7 (census E11 on S001's used-by path).
- Do-nothing base control: `fixed=1/7`, failing G1–G6 (G7 passes on the base's SOURCES.md, which is valid); matches the frozen `expect_before: c2-gate fixed=1/7 exit=1`.

## Additional observations (code evidence; not part of the eight)

- **Env override of the pins** (`counter:66-67`): `R46_PINS_OVERRIDE` replaces `PINS` from a file, and a `null` disables one pin. Tested: `R46_PINS_OVERRIDE=<{"base-knowledge-content": null}> python3 …r46-c2-gate.py --root <base-entry-one-byte-drift>` → `gate G6 pass=1 … base-intact=1`, `c2-gate fixed=7/7 exit=0`. Marked "selftests only", but the counter takes the override from the caller's environment.
- **Docstring drift**: `counter:29-30` says "the other 64 files are the round-46 tip's bytes", but the code pins 62 (errata E5 records the change, the sentence is not updated). `counter:8` says "round-46 v1.2 hardening" on a v1.1 file. Both are sentence-vs-code mismatches of the kind the kill rule names.
- **Census path**: `counter:54` hard-codes `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, a shared file outside the lane. The PINS table (`counter:56-65`) has no census entry, so G7 tracks whatever the shared script currently is. I did not test a changed census (I may not edit shared production files); this is code evidence only.
- **Census warnings do not fail G7**: `sources-census.sh:16` says exit 0 covers "clean or warnings", and W03 (mined row with used-by `—`) is a warning. A mined row with an empty used-by would pass G7. Not tested.

## Limitations

- Eight single-edit mutants, one per family; not a sweep. Not tested: a base-entry symlink to identical outside bytes (same class as F1), W03-style census warnings, S073 / F28 row content, the manifest.
- The symlink survivors use absolute targets under scratch. The "moved away" test shows the pass is external, but I did not commit a symlink to test what `git archive` on a real commit would show.
- The C1 cross-check runs C1's aggregate on the mutant tree, but C1's recheck lines `cd` into the lane (`r46-c1-gate.py:71`, `:207`), so per-entry execution reads the lane's copy. The structural limbs (L1, L2, L7) read the mutant tree. I did not resolve that interaction further.
- The env-override result is a host-environment dependence, not a tree defect.
- Lane HEAD is `0d121a2`, not `5437afe`; the working-tree corpus is identical to `5437afe`, as shown above.

## Installs / tools

None. Only `python3`, `bash`, `find`, `sha256sum`, `diff`, `ls` were used.

## Recipe (verbatim, `R46W2MutC2c/recipe.py`)

```python
#!/usr/bin/env python3
"""R46W2MutC2c recipe: single-edit mutants of the committed tip (5437afe) against r46-c2-gate.py v1.1 (G6-G7 focus)."""
import os, re, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kasegi-r46/R46W2MutC2c"
TREE = os.path.join(S, "tree")          # git archive 5437afe, never edited
BASE = os.path.join(S, "base")          # copy of the pure base export, never edited
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
COUNTER = os.path.join(LANE, "corpus/instruments/r46-c2-gate.py")   # the lane's instrument, unedited
C1 = os.path.join(LANE, "corpus/instruments/r46-c1-gate.py")
ENV = dict(os.environ, TMPDIR=os.path.join(S, "tmp"))
KN = "corpus/knowledge"
EXEMPT_ENTRY = "claim-gates.md"
BASE_ENTRY = "linux-kernel-security-bugs-reporting-process.md"


def p(d, rel):
    return os.path.join(d, rel)


def rd(path):
    with open(path, "rb") as fh:
        return fh.read()


def counter(root):
    r = subprocess.run([sys.executable, COUNTER, "--root", root], cwd=S, env=ENV, capture_output=True, text=True, timeout=600)
    gates = re.findall(r"^gate (G\d) pass=(\d) read=(.*)$", r.stdout, re.M)
    fixed = re.search(r"fixed=(\d)/7 exit=(\d)", r.stdout)
    failing = [g for g, ok, _ in gates if ok == "0"]
    return int(fixed.group(1)), int(fixed.group(2)), failing, r.stdout


def census(root):
    r = subprocess.run(["bash", "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh", "validate", "--file",
                        p(root, "corpus/SOURCES.md"), "--today", "2026-10-28"], cwd=S, env=ENV, capture_output=True, text=True)
    return r.returncode, r.stdout


# ---- mutants: each takes the copy dir d, applies ONE edit, returns (edit text, defect_present bool)
def m_dir_symlink(d):
    ext = os.path.join(S, "ext", "knowledge-copy")
    shutil.copytree(p(d, KN), ext)
    shutil.rmtree(p(d, KN))
    os.symlink(ext, p(d, KN))
    real = os.path.realpath(p(d, KN))
    # the docstring's own command, find -maxdepth 1 (default -P), now counts nothing under the symlink
    f = subprocess.run(["find", p(d, KN), "-maxdepth", "1", "-name", "*.md"], capture_output=True, text=True).stdout
    return ("corpus/knowledge replaced by a symlink to %s (identical 65 bytes, outside the tree); "
            "find(-P) lists %d files" % (ext, len(f.split()))), (not real.startswith(d) and f.strip() == "")


def m_nested_md(d):
    os.makedirs(p(d, KN + "/archive"))
    with open(p(d, KN + "/archive/old-entry.md"), "w") as fh:
        fh.write("# old\n")
    return "new file corpus/knowledge/archive/old-entry.md (nested .md, depth 2)", os.path.exists(p(d, KN + "/archive/old-entry.md"))


def m_base_drift(d):
    f = p(d, KN + "/" + BASE_ENTRY)
    before = rd(p(TREE, KN + "/" + BASE_ENTRY))
    with open(f, "wb") as fh:
        fh.write(before + b"\n")
    return "append one newline byte to %s (base entry, not exempt)" % BASE_ENTRY, rd(f) != before


def m_exempt_renamed(d):
    os.rename(p(d, KN + "/" + EXEMPT_ENTRY), p(d, KN + "/claim-gate.md"))
    return "rename %s -> claim-gate.md (bytes unchanged; exempt name is pinned)" % EXEMPT_ENTRY, \
        not os.path.exists(p(d, KN + "/" + EXEMPT_ENTRY))


def m_exempt_gutted(d):
    f = p(d, KN + "/" + EXEMPT_ENTRY)
    with open(f, "w", encoding="utf-8") as fh:
        fh.write("# claim gates\n")
    t = rd(f).decode()
    return "replace the whole body of exempt %s with one heading line" % EXEMPT_ENTRY, \
        ("## Re-ground (round 46)" not in t) and ("restoration-recheck:" not in t)


def m_census_dup_row(d):
    f = p(d, "corpus/SOURCES.md")
    lines = open(f, encoding="utf-8").read().split("\n")
    i = next(k for k, ln in enumerate(lines) if re.match(r"^\| S001 \|", ln))
    lines.insert(i + 1, lines[i])
    open(f, "w", encoding="utf-8").write("\n".join(lines))
    rc, out = census(d)
    return "append a verbatim copy of the S001 registry row directly after it (duplicate id)", "E03" in out


def m_census_dangling(d):
    f = p(d, "corpus/SOURCES.md")
    lines = open(f, encoding="utf-8").read().split("\n")
    i = next(k for k, ln in enumerate(lines) if re.match(r"^\| S001 \|", ln))
    assert lines[i].count("corpus/knowledge/cvss-v4-severity-and-vector.md") == 1
    lines[i] = lines[i].replace("corpus/knowledge/cvss-v4-severity-and-vector.md", "corpus/knowledge/cvss-v4-dangling.md")
    open(f, "w", encoding="utf-8").write("\n".join(lines))
    rc, out = census(d)
    return "S001 row (mined) used-by cell -> corpus/knowledge/cvss-v4-dangling.md (path not on disk)", "E11" in out


def m_sources_symlink(d):
    ext = os.path.join(S, "ext", "sources-root", "corpus")
    shutil.copytree(p(d, "corpus"), ext)
    os.remove(p(d, "corpus/SOURCES.md"))
    os.symlink(os.path.join(ext, "SOURCES.md"), p(d, "corpus/SOURCES.md"))
    return ("corpus/SOURCES.md replaced by a symlink to %s (identical bytes; census realpath resolves "
            "used-by against the external root)" % ext), not os.path.realpath(p(d, "corpus/SOURCES.md")).startswith(d)


MUTANTS = [
    ("knowledge-dir-symlink", m_dir_symlink),
    ("knowledge-nested-md", m_nested_md),
    ("base-entry-one-byte-drift", m_base_drift),
    ("exempt-entry-renamed", m_exempt_renamed),
    ("exempt-entry-gutted", m_exempt_gutted),
    ("census-duplicate-row", m_census_dup_row),
    ("census-dangling-usedby", m_census_dangling),
    ("sources-md-symlink-external", m_sources_symlink),
]


def fresh(name):
    d = os.path.join(S, "m", name)
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(TREE, d, symlinks=True)
    return d


def main():
    os.makedirs(os.path.join(S, "tmp"), exist_ok=True)
    rows = []
    # controls: tip copy must read 7/7; the pure base (do-nothing) must read 1/7
    d = fresh("control-tip")
    fx, ex, fail, _ = counter(d)
    print(f"control=tip-copy-no-edit rejected={int(ex != 0)} fixed={fx}/7 failing={','.join(fail) or '-'}")
    fx, ex, fail, _ = counter(BASE)
    print(f"control=do-nothing-base rejected={int(ex != 0)} fixed={fx}/7 failing={','.join(fail) or '-'}")
    for name, fn in MUTANTS:
        d = fresh(name)
        edit, present = fn(d)
        fx, ex, fail, raw = counter(d)
        rows.append((int(ex != 0), name, edit, int(present), fx, fail))
    # survivors first
    rows.sort(key=lambda r: (r[0], MUTANTS.index(next(m for m in MUTANTS if m[0] == r[1]))))
    for rej, name, edit, present, fx, fail in rows:
        print(f"mutant={name} rejected={rej} defect_present={present} fixed={fx}/7 failing={','.join(fail) or '-'} edit=[{edit}]")
    # cross-check only: does the C1 aggregate counter see the exempt-entry mutant? (C1 owns exempt content)
    d = os.path.join(S, "m", "exempt-entry-gutted")
    r = subprocess.run([sys.executable, C1, "--root", d, "--baseline", BASE], cwd=S, env=ENV, capture_output=True, text=True, timeout=900)
    m = re.search(r"c1-gate fixed=\d/7 exit=\d", r.stdout)
    print(f"cross-check=C1 mutant=exempt-entry-gutted rejected={int(r.returncode != 0)} line=[{m.group(0) if m else r.stdout.strip()[-200:]}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
