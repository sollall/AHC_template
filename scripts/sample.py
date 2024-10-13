import time

start = time.time()

try:
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from utils.inout import replace_io

    PROB_NO = sys.argv[1]
    debug_mode = True
    replace_io(PROB_NO)
except ModuleNotFoundError:
    debug_mode = False

def solve():
    for _ in range(2):
        print(input())

if __name__ == "__main__":
    solve()