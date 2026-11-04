import importlib.util, os
S="/fast/scratch/hyaku/kasegi-r68/ReviewC1"; E=S+"/export"; W=S+"/adv/w"
spec=importlib.util.spec_from_file_location("c",E+"/.ufo/waves/round-68/controls/c1-probe-run-r68.py")
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
gate=E+"/corpus/instruments/figure-audit.py"
rc,out,err=c.probe(W,gate,W+"/fixture","o1",{"id":"o1","record":"big.txt:1","recorded":"x","derive":"sort --outp=written.txt big.txt","want":"x"},dict(os.environ,TMPDIR=W))
print("ADV rc=%d written_exists=%s derive='sort --outp=written.txt big.txt' :: %s"%(rc,os.path.exists(W+"/fixture/written.txt"),(out+err).strip().splitlines()[-1][:110]))
