# executed inside probe.py's namespace after probes.py. PROBE_GATE selects the gate under test.
if os.environ.get("PROBE_GATE"):
    GATE = os.environ["PROBE_GATE"]
TAG = os.environ.get("PROBE_TAG", "")


def _py_setup_noshadow(F):
    _py_setup(F)
    os.remove(os.path.join(F, "corpus", "instruments", "json.py"))


if want("x"):
    BIG = dict(big=True)
    probe(TAG + "X01-sort-compress-equals-big", "exec", "sort --compress-program={M} -S 256K big.txt",
          "pinned: refused; base: admitted and compressor runs", fixture_kw=BIG)
    probe(TAG + "X02-sort-compress-prog-abbrev-big", "exec", "sort --compress-prog={M} -S 256K big.txt",
          "pinned: admitted? ; base: admitted, compressor runs", fixture_kw=BIG)
    probe(TAG + "X03-sort-compress-p-abbrev-big", "exec", "sort --compress-p={M} -S 256K big.txt",
          "pinned: admitted? ; base: admitted, compressor runs", fixture_kw=BIG)
    probe(TAG + "X04-sort-compress-space-big", "exec", "sort --compress-program {M} -S 256K big.txt",
          "pinned: refused; base: admitted, compressor runs", fixture_kw=BIG)
    probe(TAG + "X05-git-show-default-ext-diff", "exec", "git show HEAD",
          "repo diff.external set; NO flag: does git show run it by default?")
    probe(TAG + "X06-git-show-no-ext-diff-control", "control", "git show --no-ext-diff HEAD",
          "same repo; --no-ext-diff: expect marks 0")
    probe(TAG + "X07-nested-gate-no-shadow", "exec",
          "python3 corpus/instruments/figure-audit.py --root {F} --ledger {F}/nested.json",
          "nested gate (this GATE) re-parses ledger derive sort --compress-program=",
          setup=lambda F: (_py_setup_noshadow(F), json.dump({"figures": [{"id": "n", "record": "n", "recorded": "x",
                           "derive": "sort --compress-program=" + os.path.join(F, "mark.sh") + " -S 256K big.txt",
                           "want": "x"}]}, open(os.path.join(F, "nested.json"), "w"))),
          fixture_kw=BIG)

if want("y"):
    def _cfg_ext(F):
        git(F, "config", "diff.external", os.path.join(F, "mark.sh"))
    def _cfg_tc(F):
        git(F, "config", "diff.x.textconv", os.path.join(F, "mark.sh"))
        open(os.path.join(F, ".gitattributes"), "w").write("t.txt diff=x\n")
    probe(TAG + "Y1-ext-only-show", "exec", "git show HEAD", "diff.external only, no flag",
          fixture_kw=dict(git_config=False), setup=_cfg_ext)
    probe(TAG + "Y2-ext-only-no-ext-diff", "control", "git show --no-ext-diff HEAD", "diff.external only, --no-ext-diff: expect 0",
          fixture_kw=dict(git_config=False), setup=_cfg_ext)
    probe(TAG + "Y3-textconv-attr-show", "exec", "git show HEAD", "textconv attribute only, no flag",
          fixture_kw=dict(git_config=False), setup=_cfg_tc)
    probe(TAG + "Y4-textconv-attr-no-textconv", "control", "git show --no-textconv HEAD", "textconv attribute only, --no-textconv: expect 0",
          fixture_kw=dict(git_config=False), setup=_cfg_tc)
    probe(TAG + "Y5-textconv-attr-blob-show", "exec", "git show HEAD:t.txt", "textconv attribute only, blob show: expect 0 (G03 analogue)",
          fixture_kw=dict(git_config=False), setup=_cfg_tc)

if want("z"):
    def _fr_setup(F):
        import shutil as _sh
        d = os.path.join(F, "corpus", "instruments")
        _sh.copy("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/frontier-recheck-count.py", d)
        os.makedirs(os.path.join(F, "corpus", "knowledge"), exist_ok=True)
        open(os.path.join(F, "corpus", "README.md"), "w").write("| F01 | Probe | admitted | knowledge/e1.md | S001 |\n")
        open(os.path.join(F, "corpus", "knowledge", "e1.md"), "w").write(
            "# e1\n\nsource: S001\n\nCites S001 in prose.\n\n"
            "recheck: printf ran >> MARK; python3 -I corpus/instruments/source-recheck.py --manifest manifest.json --source S001\n")
        json.dump({"schema_version": 1, "sources": [{"id": "S001"}]}, open(os.path.join(F, "manifest.json"), "w"))
    probe(TAG + "Z1-frontier-recheck-bash-exec", "exec",
          "python3 corpus/instruments/frontier-recheck-count.py --root {F}",
          "counter admitted; bash -c runs the recheck line read from --root", setup=_fr_setup)

if want("w"):
    probe(TAG + "W02-output-cluster-r", "write", "sort -ro out.txt g.txt", "write out.txt", artifacts=("out.txt",))
    probe(TAG + "W04-output-attached", "write", "sort -oout.txt g.txt", "refused", artifacts=("out.txt",))
    probe(TAG + "W05-output-equals", "write", "sort --output=out.txt g.txt", "refused", artifacts=("out.txt",))
    probe(TAG + "W06-output-prefix", "write", "sort --outp=out.txt g.txt", "write out.txt", artifacts=("out.txt",))
    probe(TAG + "W07-output-prefix-short", "write", "sort --out out.txt g.txt", "write out.txt", artifacts=("out.txt",))
