#!/usr/bin/env python3
"""CriticC1 r68 adversarial probes: paired base/candidate gate runs, rc + reason + markers + writes."""
import json, os, shutil, subprocess, sys

W = "/fast/scratch/hyaku/kasegi-r68/CriticC1/run"
GATES = {
    "base": "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-68/controls/base-gate-d0f48405.py",
    "cand": "/fast/scratch/hyaku/kasegi-r68/CriticC1/gate-82b3b7d.py",
}


def run(argv, cwd, env=None):
    p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def lines(p):
    try:
        with open(p) as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


def snapshot(root):
    out = set()
    for b, ds, fs in os.walk(root):
        if "/.git" in b + "/" and b.endswith(".git") is False and "/.git/" in b + "/":
            continue
        for n in fs:
            out.add(os.path.relpath(os.path.join(b, n), root))
    return out


def build():
    if os.path.isdir(W):
        shutil.rmtree(W)
    os.makedirs(W)
    fx, repo = os.path.join(W, "fixture"), os.path.join(W, "repo")
    os.makedirs(fx)
    os.makedirs(repo)
    with open(os.path.join(fx, "big.txt"), "w") as f:
        f.write("".join("%07d\n" % i for i in range(60000)))
    with open(os.path.join(fx, "g.txt"), "w") as f:
        f.write("35\n")
    for name, mark, tail in (("comp.sh", "COMP_MARK", "if [ \"$1\" = -d ]; then exec gzip -dc; else exec gzip -c; fi"),
                             ("tc.sh", "TC_MARK", "exec cat \"$@\""),
                             ("smudge.sh", "SM_MARK", "exec cat"),
                             ("ext.sh", "EXT_MARK", "echo ext-diff-ran"),
                             ("pager.sh", "PG_MARK", "exec cat")):
        p = os.path.join(W, name)
        with open(p, "w") as f:
            f.write('#!/bin/sh\necho run >> "$%s"\n%s\n' % (mark, tail))
        os.chmod(p, 0o755)
    g = ["git", "-C", repo]
    assert run(g + ["init", "-q", "."], W)[0] == 0
    top = run(g + ["rev-parse", "--show-toplevel"], W)[1].strip()
    assert os.path.realpath(top) == os.path.realpath(repo), top
    ident = ["-c", "user.email=fixture@shokunin.local", "-c", "user.name=fixture"]
    for k, v in (("diff.mydriver.textconv", os.path.join(W, "tc.sh")),
                 ("diff.mydriver.binary", "false"),
                 ("filter.myfilter.smudge", os.path.join(W, "smudge.sh")),
                 ("filter.myfilter.clean", "cat"),
                 ("diff.external", os.path.join(W, "ext.sh")),
                 ("core.pager", os.path.join(W, "pager.sh"))):
        assert run(g + ["config", k, v], W)[0] == 0
    with open(os.path.join(repo, "big.txt"), "w") as f:
        f.write("x" * 1000 + "\n")
    with open(os.path.join(repo, "f.txt"), "w") as f:
        f.write("filtered\n")
    with open(os.path.join(repo, ".gitattributes"), "w") as f:
        f.write("big.txt diff=mydriver\nf.txt filter=myfilter\n")
    assert run(g + ["add", "-A"], W)[0] == 0
    assert run(g + ident + ["commit", "-qm", "one"], W)[0] == 0
    # second commit modifying big.txt so `git show HEAD` emits a patch for it
    with open(os.path.join(repo, "big.txt"), "w") as f:
        f.write("y" * 1000 + "\n")
    assert run(g + ["add", "-A"], W)[0] == 0
    assert run(g + ident + ["commit", "-qm", "two"], W)[0] == 0
    # merge commit touching big.txt on both sides for -c/--cc
    assert run(g + ["branch", "side", "HEAD~1"], W)[0] == 0
    assert run(g + ["checkout", "-q", "side"], W)[0] == 0
    with open(os.path.join(repo, "big.txt"), "w") as f:
        f.write("z" * 1000 + "\n")
    assert run(g + ident + ["commit", "-qam", "side"], W)[0] == 0
    assert run(g + ["checkout", "-q", "-"], W)[0] in (0,)
    run(g + ident + ["merge", "-q", "side", "-m", "m"], W)
    with open(os.path.join(repo, "big.txt"), "w") as f:
        f.write("m" * 1000 + "\n")
    assert run(g + ["add", "-A"], W)[0] == 0
    assert run(g + ident + ["commit", "-qm", "merge"], W)[0] == 0
    return fx, repo


PROBES = [
    # (id, root, derive) ; root in {"fx","repo"}; COMP placeholder = compressor path
    # --- sort compress-program spellings
    ("s-exact-eq", "fx", "sort --compress-program=COMP -S 1K big.txt | head -n 1"),
    ("s-abbr-compress-progra", "fx", "sort --compress-progra=COMP -S 1K big.txt | head -n 1"),
    ("s-abbr-compress-p", "fx", "sort --compress-p=COMP -S 1K big.txt | head -n 1"),
    ("s-abbr-compress", "fx", "sort --compress=COMP -S 1K big.txt | head -n 1"),
    ("s-abbr-comp", "fx", "sort --comp=COMP -S 1K big.txt | head -n 1"),
    ("s-abbr-co", "fx", "sort --co=COMP -S 1K big.txt | head -n 1"),
    ("s-abbr-space", "fx", "sort --compress-progr COMP -S 1K big.txt | head -n 1"),
    ("s-dq", "fx", 'sort "--compress-program=COMP" -S 1K big.txt | head -n 1'),
    ("s-sq-split", "fx", "sort --compress-'program'=COMP -S 1K big.txt | head -n 1"),
    ("s-bs", "fx", r"sort --compress-progra\m=COMP -S 1K big.txt | head -n 1"),
    ("s-ansi-c", "fx", "sort $'--compress-program=COMP' -S 1K big.txt | head -n 1"),
    ("s-after-ddash", "fx", "sort -S 1K -- big.txt --compress-program=COMP | head -n 1"),
    # --- sort write spellings (pre-existing write class)
    ("s-o-bundled-uo", "fx", "sort -uo OUT1 g.txt && cat g.txt"),
    ("s-o-bundled-ro", "fx", "sort -ro OUT2 g.txt && cat g.txt"),
    ("s-output-abbr", "fx", "sort --outp=OUT3 g.txt && cat g.txt"),
    ("s-output-abbr-o", "fx", "sort --o=OUT4 g.txt && cat g.txt"),
    ("s-tempdir", "fx", "sort -S 1K -T TDIR big.txt | head -n 1"),
    # --- git show textconv family
    ("g-textconv", "repo", "git show --textconv HEAD:big.txt | head -n 1"),
    ("g-textcon", "repo", "git show --textcon HEAD:big.txt | head -n 1"),
    ("g-textc", "repo", "git show --textc HEAD:big.txt | head -n 1"),
    ("g-show-commit-default", "repo", "git show HEAD~1 | grep -c y"),
    ("g-show-commit-stat", "repo", "git show --stat HEAD~1 | head -n 1"),
    ("g-show-c-merge", "repo", "git show -c HEAD | grep -c m"),
    ("g-show-cc-merge", "repo", "git show --cc HEAD | grep -c m"),
    ("g-show-m", "repo", "git show -m HEAD | grep -c m"),
    ("g-show-filters", "repo", "git show --filters HEAD:f.txt | head -n 1"),
    ("g-show-blob-plain", "repo", "git show HEAD:big.txt | head -n 1"),
    ("g-show-blob-f", "repo", "git show HEAD:f.txt | head -n 1"),
    ("g-catfile-textconv", "repo", "git cat-file --textconv HEAD:big.txt | head -n 1"),
    ("g-catfile-filters", "repo", "git cat-file --filters HEAD:f.txt | head -n 1"),
    ("g-catfile-p", "repo", "git cat-file -p HEAD:big.txt | head -n 1"),
    ("g-ext-diff", "repo", "git show --ext-diff HEAD~1 | head -n 1"),
    ("g-ext-dif-abbr", "repo", "git show --ext-dif HEAD~1 | head -n 1"),
    ("g-output-abbr", "repo", "git show --outpu=OUT5 HEAD && cat big.txt"),
    ("g-env-pager", "repo", "GIT_PAGER=cat git show HEAD | head -n 1"),
    ("g-env-extdiff", "repo", "GIT_EXTERNAL_DIFF=EXT git show HEAD | head -n 1"),
    ("g-dash-c", "repo", "git -c core.pager=cat show HEAD | head -n 1"),
    ("g-paginate", "repo", "git -p show HEAD | head -n 1"),
    # --- other heads
        ("h-ls-R", "fx", "ls | wc -l"),
    ("h-wc-files0", "fx", "wc --files0-from=g.txt"),
    ("h-sha-check", "fx", "sha256sum -c g.txt"),
    ("h-cut", "fx", "cut -c1 g.txt"),
    ("h-tr", "fx", "tr 3 4 < g.txt"),
    ("h-grep-r", "fx", "grep -r 35 . | wc -l"),
]


def main():
    fx, repo = build()
    roots = {"fx": fx, "repo": repo}
    results = []
    for gname, gate in GATES.items():
        for pid, rk, derive in PROBES:
            root = roots[rk]
            marks = {}
            env = dict(os.environ)
            for m in ("COMP_MARK", "TC_MARK", "SM_MARK", "EXT_MARK", "PG_MARK"):
                path = os.path.join(W, "m.%s.%s.%s" % (gname, pid, m))
                open(path, "w").close()
                marks[m] = path
                env[m] = path
            tdir = os.path.join(W, "tdir.%s.%s" % (gname, pid))
            os.makedirs(tdir)
            env["TMPDIR"] = os.path.join(W, "tmp")
            os.makedirs(env["TMPDIR"], exist_ok=True)
            d = derive.replace("COMP", os.path.join(W, "comp.sh")).replace("EXT", os.path.join(W, "ext.sh")) \
                .replace("TDIR", tdir)
            outs = {}
            for i in range(1, 6):
                o = os.path.join(W, "out%d.%s.%s" % (i, gname, pid))
                outs["OUT%d" % i] = o
                d = d.replace("OUT%d" % i, o)
            led = os.path.join(W, "led.%s.%s.json" % (gname, pid))
            with open(led, "w") as f:
                json.dump({"figures": [{"id": pid, "record": "x", "recorded": "?", "derive": d, "want": "__nomatch__"}]}, f)
            try:
                rc, out, err = run([sys.executable, gate, "--ledger", led, "--root", root], W, env=env)
            except subprocess.TimeoutExpired:
                rc, out, err = "TIMEOUT", "", ""
            reason = ""
            for ln in (err + "\n" + out).splitlines():
                if "reason=" in ln:
                    reason = ln.split("reason=", 1)[1].split()[0]
                    break
                if ln.startswith("FIG "):
                    reason = "derived=" + ln.split("derived=", 1)[1].split(" want=")[0][:40]
            m = {k[:-5]: lines(v) for k, v in marks.items()}
            wrote = [k for k, v in outs.items() if os.path.exists(v)]
            row = {"gate": gname, "id": pid, "rc": rc, "reason": reason,
                   "marks": {k: v for k, v in m.items() if v}, "wrote": wrote,
                   "executed": any(m.values()) or bool(wrote), "derive": derive}
            results.append(row)
            print("PROBE gate=%s id=%s rc=%s reason=%s marks=%s wrote=%s" % (
                gname, pid, rc, reason, row["marks"] or "{}", ",".join(wrote) or "-"))
    with open("/fast/scratch/hyaku/kasegi-r68/CriticC1/results.json", "w") as f:
        json.dump(results, f, indent=1)


main()
