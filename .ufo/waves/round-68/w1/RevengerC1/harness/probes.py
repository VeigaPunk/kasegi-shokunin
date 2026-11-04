# probes (exec'd inside probe.py): one fixture, one derive, one verdict per call.
GROUP = sys.argv[2] if len(sys.argv) > 2 else "all"


def want(g):
    return GROUP == "all" or GROUP == g


# ---------- sort (uutils sort 0.8.0, clap-style parser) ----------
if want("sort"):
    probe("S01-compress-equals", "exec", "sort --compress-program={M} g.txt", "refused")
    probe("S02-compress-space", "exec", "sort --compress-program {M} g.txt", "refused")
    probe("S03-compress-quoted", "exec", "sort '--compress-program={M}' g.txt", "refused")
    probe("S04-compress-prefix-equals", "exec", "sort --compress-prog={M} g.txt", "ADMITTED? (getopt-style abbrev)")
    probe("S05-compress-prefix-short", "exec", "sort --compress-p={M} g.txt", "ADMITTED? (abbrev)")
    probe("S06-compress-after-buffer", "exec", "sort -S 1K --compress-program={M} g.txt", "refused")
    probe("S07-compress-short-cluster", "exec", "sort -S1K -r --compress-program={M} g.txt", "refused")
    probe("S00-control-plain", "control", "sort -S 1K g.txt", "admitted, marks 0")
    probe("S08-compress-attached-shell-word", "exec", "sort --compress-program={M}g.txt g.txt", "admitted? marks?",
          note="argument spelled with the prefix; the program path is only partly the marker")
    probe("W01-output-short", "write", "sort -o out.txt g.txt", "refused", artifacts=("out.txt",))
    probe("W02-output-cluster-r", "write", "sort -ro out.txt g.txt", "ADMITTED? write out.txt", artifacts=("out.txt",))
    probe("W03-output-cluster-u", "write", "sort -uo out.txt g.txt", "ADMITTED? write out.txt", artifacts=("out.txt",))
    probe("W04-output-attached", "write", "sort -oout.txt g.txt", "refused", artifacts=("out.txt",))
    probe("W05-output-equals", "write", "sort --output=out.txt g.txt", "refused", artifacts=("out.txt",))
    probe("W06-output-prefix", "write", "sort --outp=out.txt g.txt", "ADMITTED? write out.txt", artifacts=("out.txt",))
    probe("W07-output-prefix-short", "write", "sort --out out.txt g.txt", "ADMITTED? write out.txt", artifacts=("out.txt",))
    probe("W08-tempdir-explicit", "write", "sort -T td -S 1K big.txt", "admitted; temp writes under td",
          fixture_kw=dict(big=True), artifacts=(), note="strace openat under td expected")
    probe("W09-tempdir-long", "write", "sort --temporary-directory=td -S 1K big.txt", "admitted; temp writes under td",
          fixture_kw=dict(big=True))
    probe("W10-tmpdir-env", "write", "sort -S 1K big.txt", "admitted; TMPDIR-controlled temp writes",
          fixture_kw=dict(big=True), env={"TMPDIR": "{F}/td"})
    probe("R01-sort-outside-read", "read", "sort /etc/hostname", "admitted; read outside lane")

# ---------- git show ----------
if want("git"):
    probe("G01-show-textconv", "exec", "git show --textconv HEAD:t.txt", "refused")
    probe("G02-show-textconv-prefix", "exec", "git show --textc HEAD:t.txt", "ADMITTED? (parse-options abbrev)")
    probe("G03-show-default-textconv", "exec", "git show HEAD:t.txt", "no flag; attribute textconv",
          note="does default git show run textconv?")
    probe("G04-show-no-textconv-control", "control", "git show --no-textconv HEAD:t.txt", "admitted, marks 0")
    probe("G05-show-ext-diff", "exec", "git show --ext-diff HEAD", "refused")
    probe("G06-show-ext-diff-prefix", "exec", "git show --ext-d HEAD", "ADMITTED? (abbrev)")
    probe("G07-show-output-equals", "write", "git show --output=o.txt HEAD", "refused", artifacts=("o.txt",))
    probe("G08-show-output-prefix", "write", "git show --outp=o.txt HEAD", "ADMITTED? write o.txt", artifacts=("o.txt",))
    probe("G09-show-plain-commit", "control", "git show HEAD", "control, diff of commit, no ext diff")
    probe("G10-cat-file-textconv", "exec", "git cat-file --textconv HEAD:t.txt", "admitted? (not in DENIED_FLAGS)")
    probe("G11-cat-file-filters", "exec", "git cat-file --filters --path=t.txt HEAD", "admitted? smudge filter")
    probe("G12-cat-file-p-control", "control", "git cat-file -p HEAD:t.txt", "admitted, marks 0")
    probe("G13-cat-file-batch-textconv", "exec", "git cat-file --batch --textconv < list.txt", "admitted? textconv batch",
          setup=lambda F: open(os.path.join(F, "list.txt"), "w").write("HEAD:t.txt\n"))
    probe("G14-ls-tree-control", "control", "git ls-tree -r HEAD", "admitted, marks 0")
    probe("G15-ls-tree-format", "read", "git ls-tree --format=%(objectname) HEAD", "admitted, read-only")
    probe("G16-git-c-config", "exec", "git -c diff.x.textconv={M} show HEAD:t.txt", "refused (-c not a subcommand)")
    probe("G17-git-C-dir", "exec", "git -C {F} show --textconv HEAD:t.txt", "refused")
    probe("G18-git-show-separator", "exec", "git show -- --textconv", "refused? (denied scan)")
    probe("G19-git-show-config-after-subcmd", "exec", "git show -c diff.x.textconv={M} HEAD:t.txt", "?")
    probe("G20-cat-file-textconv-attribute", "exec", "git cat-file --filters HEAD:t.txt", "smudge via attributes, no path")

# ---------- environment-controlled (not reachable through the derive grammar) ----------
if want("env"):
    probe("E01-env-prefix-refused", "env", "GIT_EXTERNAL_DIFF={M} git show HEAD", "refused (env assignment head)")
    probe("E02-env-config-count-show", "env", "git show HEAD:t.txt", "env injects textconv w/o repo config",
          fixture_kw=dict(git_config=False), env={"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "diff.x.textconv",
                                                  "GIT_CONFIG_VALUE_0": "{M}"},
          setup=lambda F: open(os.path.join(F, ".gitattributes"), "w").write("t.txt diff=x\n"))
    probe("E03-env-external-diff-show-commit", "env", "git show HEAD", "GIT_EXTERNAL_DIFF w/o --ext-diff",
          env={"GIT_EXTERNAL_DIFF": "{M}"})
    probe("E04-env-sort-compress-env-none", "env", "sort -S 1K g.txt", "no env-sort exec path", env={})

# ---------- read-only heads outside the lane ----------
if want("ro"):
    probe("R02-cat-outside", "read", "cat /etc/hostname", "admitted; read outside lane")
    probe("R03-head-outside", "read", "head -n 1 /etc/hostname", "admitted; read outside lane")
    probe("R04-grep-file-from-outside", "read", "grep -f /etc/hostname g.txt", "admitted; read outside lane")
    probe("R05-ls-root", "read", "ls /", "admitted; read outside lane")
    probe("R06-sha256-outside", "read", "sha256sum /etc/hostname", "admitted; read outside lane")
    probe("R07-wc-files0-from-outside", "read", "wc --files0-from=/etc/hostname", "admitted? read")
    probe("R08-tr-cut-control", "control", "cut -c1 g.txt | tr a-z A-Z", "admitted control")

# ---------- python head ----------
def _py_setup(F):
    d = os.path.join(F, "corpus", "instruments")
    open(os.path.join(d, "probe-ok.py"), "w").write("print(35)\n")
    open(os.path.join(d, "probe-helper.py"), "w").write("X = 1\n")
    open(os.path.join(d, "probe-imp.py"), "w").write("import probe_helper\nprint(35)\n")
    open(os.path.join(d, "probe_helper.py"), "w").write("X = 1\n")
    open(os.path.join(d, "json.py"), "w").write(
        "import os\nopen(os.path.join(os.path.dirname(__file__), '..', '..', 'MARK'), 'a').write('ran\\n')\n")
    open(os.path.join(d, "probe-shadow.py"), "w").write("import json\nprint(35)\n")
    open(os.path.join(d, "probe-exit.py"), "w").write("import sys\nsys.exit(0)\n")
    shutil.copy("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py",
                os.path.join(d, "capture-source.py"))
    shutil.copy(GATE, os.path.join(d, "figure-audit.py"))
    open(os.path.join(F, "src.txt"), "w").write("Alpha beta gamma delta epsilon zeta eta theta iota kappa.\n")


if want("py"):
    probe("P01-py-control", "control", "python3 corpus/instruments/probe-ok.py", "admitted, prints 35", setup=_py_setup)
    probe("P02-py-dash-c", "exec", "python3 -c 'print(1)'", "refused", setup=_py_setup)
    probe("P03-py-dash-I", "exec", "python3 -I corpus/instruments/probe-ok.py", "refused", setup=_py_setup)
    probe("P04-py-dash-m", "exec", "python3 -m json.tool g.txt", "refused", setup=_py_setup)
    probe("P05-py-traversal", "exec", "python3 corpus/instruments/../../probe-ok.py", "refused? (realpath check)", setup=_py_setup)
    probe("P06-py-env-prefix", "env", "PYTHONPATH={F}/envpy python3 corpus/instruments/probe-ok.py", "refused (env head)", setup=_py_setup)
    probe("P07-py-pycache-write", "write", "python3 corpus/instruments/probe-imp.py", "admitted; writes __pycache__",
          setup=_py_setup, artifacts=("corpus/instruments/__pycache__/probe_helper.cpython-314.pyc",))
    probe("P08-py-sys-path-shadow", "exec", "python3 corpus/instruments/probe-shadow.py", "admitted; in-tree json.py shadows stdlib",
          setup=_py_setup)
    probe("P09-py-capture-egress-write-outside", "write+read",
          "python3 corpus/instruments/capture-source.py --id x --url file://{F}/src.txt --out " + OUTSIDE + "/cap-outside.txt --kind text",
          "admitted; reads file:// URL (any scheme urllib takes) and writes outside root",
          setup=_py_setup, artifacts=(), note="check " + OUTSIDE + "/cap-outside.txt")
    probe("P10-py-nested-gate-refuses-compress", "exec", "python3 corpus/instruments/figure-audit.py --root {F} --ledger {F}/nested.json",
          "admitted; nested gate re-parses ledger derives",
          setup=lambda F: (_py_setup(F), json.dump({"figures": [{"id": "n", "record": "n", "recorded": "x",
                                                    "derive": "sort --compress-program=" + os.path.join(F, "mark.sh") + " g.txt", "want": "x"}]},
                                                   open(os.path.join(F, "nested.json"), "w"))))
    probe("P11-py-exit-control", "control", "python3 corpus/instruments/probe-exit.py", "admitted; exit 0 but no stdout => stale", setup=_py_setup)
    probe("P12-py-env-pythonpath-sitecustomize", "env", "python3 corpus/instruments/probe-ok.py",
          "env PYTHONPATH sitecustomize runs before script", setup=lambda F: (_py_setup(F), os.makedirs(os.path.join(F, "envpy"), exist_ok=True),
          open(os.path.join(F, "envpy", "sitecustomize.py"), "w").write("open(%r,'a').write('ran\\n')\n" % os.path.join(F, "MARK"))),
          env={"PYTHONPATH": "{F}/envpy"})
