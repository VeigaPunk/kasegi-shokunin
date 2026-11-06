import sys
V = f"""A
B{1 +  # mutbat-ab
1}C"""
def selftest():
    assert V == "A\nB1C"
    print("selftest cases=1 failures=0")
    return 0
if __name__ == "__main__":
    sys.exit(selftest())
