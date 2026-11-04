exec(compile(open('/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-63/w1/MutationCollector/harness-attacks.py').read().split("run('pristine'")[0], 'setup', 'exec'))
run('pristine-same-mode',I,S/'same-pristine',expected=0)
try:
 I.write_bytes((W/'always-green.py').read_bytes())
 print('mutant_sha256='+sha(I),flush=True)
 run('always-green-same-mode',I,S/'same-mutated',expected=1)
finally:
 I.write_bytes(original)
 print('restored_sha256='+sha(I)+' equals_before='+str(I.read_bytes()==original),flush=True)
 run('restored-same-mode',I,S/'same-restored',expected=0)
