import os, signal, sys
print("1"); print("2"); print("3"); sys.stdout.flush()
os.kill(os.getpid(), signal.SIGKILL)
