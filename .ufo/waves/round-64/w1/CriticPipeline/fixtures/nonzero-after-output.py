import sys
print("5")
sys.stdout.flush()
raise RuntimeError("counter crashed after printing")
